import asyncio
import re
import sys
from pathlib import Path
from typing import Optional

from playwright.async_api import (
    BrowserContext,
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
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        self._lock = asyncio.Lock()

    async def open_session(self) -> FlowSessionStatus:
        page = await self._ensure_page()
        if not page.url.startswith(settings.GOOGLE_FLOW_URL):
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
        if self._context is not None:
            await self._context.close()
        if self._playwright is not None:
            await self._playwright.stop()
        self._context = None
        self._playwright = None
        self._page = None

    async def _ensure_page(self) -> Page:
        if self._page is not None and not self._page.is_closed():
            return self._page

        self._playwright = await async_playwright().start()
        launch_args: dict = {
            "user_data_dir": str(settings.CHROME_PROFILE_DIR),
            "headless": settings.BROWSER_HEADLESS,
            "accept_downloads": True,
            "viewport": {"width": 1440, "height": 1000},
        }
        chrome_path = Path(settings.CHROME_EXECUTABLE_PATH)
        if chrome_path.is_file():
            launch_args["executable_path"] = str(chrome_path)

        self._context = await self._playwright.chromium.launch_persistent_context(
            **launch_args
        )
        self._page = self._context.pages[0] if self._context.pages else await self._context.new_page()
        self._page.set_default_timeout(settings.BROWSER_TIMEOUT_MS)
        return self._page

    async def _find_prompt(self, page: Page) -> Optional[Locator]:
        for selector in self._prompt_selectors:
            locator = page.locator(selector)
            for index in range(await locator.count()):
                candidate = locator.nth(index)
                if await candidate.is_visible() and await candidate.is_editable():
                    return candidate
        return None

    async def _fill_prompt(self, locator: Locator, prompt: str) -> None:
        tag = await locator.evaluate("element => element.tagName.toLowerCase()")
        if tag in ("textarea", "input"):
            await locator.fill(prompt)
            return
        await locator.click()
        await locator.press("Meta+A" if sys.platform == "darwin" else "Control+A")
        await locator.insert_text(prompt)

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
