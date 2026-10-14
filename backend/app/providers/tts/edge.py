from pathlib import Path

import edge_tts

from app.core.config import settings


class EdgeTTSService:
    async def synthesize(
        self,
        text: str,
        audio_path: Path,
        subtitle_path: Path,
        voice: str | None = None,
    ) -> None:
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        subtitle_path.parent.mkdir(parents=True, exist_ok=True)
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice or settings.DEFAULT_TTS_VOICE,
            rate=settings.DEFAULT_TTS_RATE,
            pitch=settings.DEFAULT_TTS_PITCH,
            boundary="SentenceBoundary",
        )
        subtitles = edge_tts.SubMaker()
        with audio_path.open("wb") as audio_file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_file.write(chunk["data"])
                elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                    subtitles.feed(chunk)

        subtitle_text = subtitles.get_srt().strip()
        if not subtitle_text:
            subtitle_text = "1\n00:00:00,000 --> 00:00:10,000\n" + text.strip()
        subtitle_path.write_text(subtitle_text + "\n", encoding="utf-8")
