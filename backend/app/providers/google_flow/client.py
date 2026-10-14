import asyncio
import re
import sys
from pathlib import Path
from typing import Optional

import httpx
from playwright.async_api import (
    Browser,
    BrowserContext,
    Error as PlaywrightError,
    Locator,
    Page,
    Playwright,
    TimeoutError as PlaywrightTimeoutError,
    async_playwright,
)

from app.core.config import settings
from app.schemas.pipeline import FlowSessionStatus


class FlowUserActionRequired(RuntimeError):
    pass


class GoogleFlowClient:
    """Drive the user's own Google Flow session through a persistent browser."""

    _prompt_selectors = (
        "textarea[placeholder*='prompt' i]",
        "[contenteditable='true'][role='textbox']",
        "textarea",
        "[contenteditable='true']",
    )

    def __init__(self) -> None:
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        self._browser_process: Optional[asyncio.subprocess.Process] = None
        self._lock = asyncio.Lock()

    async def open_session(self) -> FlowSessionStatus:
        page = await self._ensure_page()
        if not self._is_flow_url(page.url) and "accounts.google.com" not in page.url:
            await page.goto(
                settings.GOOGLE_FLOW_URL,
                wait_until="domcontentloaded",
                timeout=max(settings.BROWSER_TIMEOUT_MS, 60000),
            )
        await page.bring_to_front()
        return await self.status()

    async def status(self) -> FlowSessionStatus:
        if self._page is None or self._page.is_closed():
            return FlowSessionStatus(
                open=False,
                ready=False,
                message="Trình duyệt Flow chưa được mở.",
            )

        prompt = await self._find_prompt(self._page)
        ready = prompt is not None
        message = (
            "Flow đã sẵn sàng nhận prompt."
            if ready
            else "Hãy đăng nhập Google, mở hoặc tạo một Flow project, rồi để cửa sổ này mở."
        )
        return FlowSessionStatus(
            open=True,
            ready=ready,
            url=self._page.url,
            message=message,
        )

    async def generate_image(
        self,
        prompt: str,
        destination_dir: Path,
        scene_order: int,
    ) -> Path:
        async with self._lock:
            page = await self._ensure_page()
            prompt_box = await self._find_prompt(page)
            if prompt_box is None:
                raise FlowUserActionRequired(
                    "Flow chưa sẵn sàng. Hãy đăng nhập, mở một project và chọn chế độ tạo Image."
                )

            destination_dir.mkdir(parents=True, exist_ok=True)
            baseline_images = await page.locator("img").count()
            baseline_downloads = await self._download_button_count(page)

            await self._fill_prompt(prompt_box, prompt)
            generate_button = await self._find_generate_button(page)
            if generate_button is None:
                raise FlowUserActionRequired(
                    "Không tìm thấy nút Generate. Hãy chọn chế độ Image trong Flow rồi thử tiếp tục."
                )
            await generate_button.click()

            timeout_seconds = settings.FLOW_GENERATION_TIMEOUT_MS / 1000
            deadline = asyncio.get_running_loop().time() + timeout_seconds
            while asyncio.get_running_loop().time() < deadline:
                await asyncio.sleep(2)
                if await self._download_button_count(page) > baseline_downloads:
                    break
                if await page.locator("img").count() > baseline_images:
                    await asyncio.sleep(3)
                    break
            else:
                await self._save_debug_screenshot(page, destination_dir, scene_order)
                raise FlowUserActionRequired(
                    "Flow chưa trả ảnh trong thời gian chờ. Kiểm tra credit, cảnh báo nội dung hoặc CAPTCHA trên cửa sổ Flow."
                )

            try:
                return await self._download_latest_image(
                    page,
                    destination_dir,
                    scene_order,
                )
            except FlowUserActionRequired:
                await self._save_debug_screenshot(page, destination_dir, scene_order)
                raise

    async def close(self) -> None:
        # Chromium runs independently so a backend hot reload can reconnect to it.
        # Stopping Playwright disconnects CDP without closing the user's Flow window.
        if self._playwright is not None:
            await self._playwright.stop()
        self._browser = None
        self._context = None
        self._playwright = None
        self._page = None

    async def _ensure_page(self) -> Page:
        if self._page is not None and not self._page.is_closed():
            return self._page

        if self._context is not None:
            try:
                pages = [page for page in self._context.pages if not page.is_closed()]
                self._page = pages[0] if pages else await self._context.new_page()
                self._page.set_default_timeout(settings.BROWSER_TIMEOUT_MS)
                return self._page
            except Exception:
                self._browser = None
                self._context = None
                self._page = None

        if self._playwright is None:
            self._playwright = await async_playwright().start()

        if not await self._connect_to_browser():
            await self._start_browser()
            for _ in range(40):
                if await self._connect_to_browser():
                    break
                await asyncio.sleep(0.25)
            else:
                raise RuntimeError(
                    "Chromium đã mở nhưng backend không kết nối được cổng điều khiển."
                )

        assert self._context is not None
        pages = [page for page in self._context.pages if not page.is_closed()]
        self._page = pages[0] if pages else await self._context.new_page()
        self._page.set_default_timeout(settings.BROWSER_TIMEOUT_MS)
        return self._page

    async def _connect_to_browser(self) -> bool:
        assert self._playwright is not None
        endpoint = self._cdp_endpoint
        if not await self._cdp_is_ready():
            return False
        try:
            self._browser = await self._playwright.chromium.connect_over_cdp(
                endpoint,
                timeout=5000,
            )
        except Exception:
            return False
        if not self._browser.contexts:
            return False
        self._context = self._browser.contexts[0]
        return True

    async def _start_browser(self) -> None:
        assert self._playwright is not None
        chrome_path = Path(settings.CHROME_EXECUTABLE_PATH)
        executable = (
            str(chrome_path)
            if chrome_path.is_file()
            else self._playwright.chromium.executable_path
        )
        settings.CHROME_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
        arguments = [
            executable,
            f"--remote-debugging-port={settings.FLOW_REMOTE_DEBUGGING_PORT}",
            f"--user-data-dir={settings.CHROME_PROFILE_DIR}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-background-mode",
            settings.GOOGLE_FLOW_URL,
        ]
        if settings.BROWSER_HEADLESS:
            arguments.insert(-1, "--headless=new")
        self._browser_process = await asyncio.create_subprocess_exec(
            *arguments,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        for _ in range(60):
            if await self._cdp_is_ready():
                return
            if self._browser_process.returncode is not None:
                raise RuntimeError(
                    f"Chromium đóng ngay sau khi khởi động (mã {self._browser_process.returncode})."
                )
            await asyncio.sleep(0.25)
        raise RuntimeError("Chromium không mở cổng điều khiển sau 15 giây.")

    async def _cdp_is_ready(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=1.0) as client:
                response = await client.get(f"{self._cdp_endpoint}/json/version")
                return response.status_code == 200
        except httpx.HTTPError:
            return False

    @property
    def _cdp_endpoint(self) -> str:
        return f"http://127.0.0.1:{settings.FLOW_REMOTE_DEBUGGING_PORT}"

    @staticmethod
    def _is_flow_url(url: str) -> bool:
        return "flow.google.com" in url or ("labs.google" in url and "/flow" in url)

    async def _find_prompt(self, page: Page) -> Optional[Locator]:
        for selector in self._prompt_selectors:
            locator = page.locator(selector)
            for index in range(await locator.count()):
                candidate = locator.nth(index)
                if await candidate.is_visible() and await candidate.is_editable():
                    return candidate
        return None

    async def _fill_prompt(self, locator: Locator, prompt: str) -> None:
        try:
            await locator.fill(prompt)
            return
        except PlaywrightError:
            # Some Flow editor variants use a custom contenteditable surface
            # that does not implement the native value setter used by fill().
            pass

        await locator.click()
        await locator.press("Meta+A" if sys.platform == "darwin" else "Control+A")
        await locator.press_sequentially(prompt, delay=1)

    async def _find_generate_button(self, page: Page) -> Optional[Locator]:
        patterns = (
            re.compile(r"^(generate image|generate|tạo ảnh|tạo|gửi)$", re.I),
            re.compile(r"generate|tạo ảnh", re.I),
        )
        for pattern in patterns:
            locator = page.get_by_role("button", name=pattern)
            for index in reversed(range(await locator.count())):
                candidate = locator.nth(index)
                if await candidate.is_visible() and await candidate.is_enabled():
                    return candidate

        fallback = page.locator("button[type='submit']")
        for index in reversed(range(await fallback.count())):
            candidate = fallback.nth(index)
            if await candidate.is_visible() and await candidate.is_enabled():
                return candidate
        return None

    async def _download_button_count(self, page: Page) -> int:
        return await page.get_by_role(
            "button",
            name=re.compile(r"download|tải xuống", re.I),
        ).count()

    async def _download_latest_image(
        self,
        page: Page,
        destination_dir: Path,
        scene_order: int,
    ) -> Path:
        buttons = page.get_by_role(
            "button",
            name=re.compile(r"download|tải xuống", re.I),
        )
        button = await self._last_visible(buttons)

        if button is None:
            images = page.locator("img")
            for index in reversed(range(await images.count())):
                image = images.nth(index)
                if await image.is_visible():
                    await image.hover()
                    await image.click()
                    await page.wait_for_timeout(800)
                    button = await self._last_visible(buttons)
                    if button is not None:
                        break

        if button is None:
            raise FlowUserActionRequired(
                "Ảnh đã tạo nhưng chưa tìm thấy nút Download. Hãy mở ảnh mới nhất trong Flow rồi bấm Tiếp tục."
            )

        try:
            async with page.expect_download(timeout=20000) as download_info:
                await button.click()
            download = await download_info.value
        except PlaywrightTimeoutError as exc:
            raise FlowUserActionRequired(
                "Flow chưa bắt đầu tải ảnh. Hãy kiểm tra ảnh mới nhất và quyền tải xuống."
            ) from exc

        suffix = Path(download.suggested_filename).suffix.lower()
        if suffix not in (".png", ".jpg", ".jpeg", ".webp"):
            suffix = ".png"
        destination = destination_dir / f"scene_{scene_order:03d}{suffix}"
        await download.save_as(str(destination))
        return destination

    async def _last_visible(self, locator: Locator) -> Optional[Locator]:
        for index in reversed(range(await locator.count())):
            candidate = locator.nth(index)
            if await candidate.is_visible():
                return candidate
        return None

    async def _save_debug_screenshot(
        self,
        page: Page,
        destination_dir: Path,
        scene_order: int,
    ) -> None:
        debug_dir = destination_dir.parent / "debug"
        debug_dir.mkdir(parents=True, exist_ok=True)
        try:
            await page.screenshot(
                path=str(debug_dir / f"flow_scene_{scene_order:03d}.png"),
                full_page=False,
            )
        except Exception:
            pass
