import pyttsx3
from threading import Lock

class SpeechEngine:
    """
    Minimal wrapper around pyttsx3 so calls from any thread are safe.
    """

    def __init__(self, rate: int = 180, volume: float = 1.0, voice: str | None = None):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)
        if voice:
            self.engine.setProperty("voice", voice)
        self._lock = Lock()   # pyttsx3 isn't thread-safe by default

    def say(self, text: str) -> None:
        with self._lock:
            self.engine.say(text)
            self.engine.runAndWait()
            import pyttsx3
from gtts import gTTS
from pathlib import Path
import tempfile
import subprocess
from threading import Lock
from typing import Optional


class SpeechEngine:
    """
    Tries offline pyttsx3 first (if system voice supports the language).
    Falls back to gTTS + playsound for any ISO-639-1 `lang`, e.g. 'en', 'hi'.
    """

    def __init__(
        self,
        rate: int = 180,
        volume: float = 1.0,
        lang: str = "en",
        voice_id: Optional[str] = None,
    ):
        self.lang = lang
        self._lock = Lock()

        # ---------- pyttsx3 ----------
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)

        # Pick voice by id OR by language substring in its name
        chosen = None
        for v in self.engine.getProperty("voices"):
            if voice_id and v.id == voice_id:
                chosen = v.id
                break
            if voice_id is None and lang in v.name.lower():
                chosen = v.id
        if chosen:
            self.engine.setProperty("voice", chosen)

        # If no voice supports the language, we’ll switch to gTTS
        self._offline_ok = chosen is not None and lang in self.engine.getProperty(
            "voice"
        ).lower()

    # ---------- public API ----------
    def say(self, text: str) -> None:
        with self._lock:
            if self._offline_ok:
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                # gTTS fallback
                mp3_path = self._make_gtts_mp3(text)
                # playsound is the simplest cross-platform 1-liner
                subprocess.run(["python", "-m", "playsound", str(mp3_path)], check=True)
                mp3_path.unlink(missing_ok=True)

    # ---------- helpers ----------
    def _make_gtts_mp3(self, text: str) -> Path:
        tts = gTTS(text=text, lang=self.lang)
        tmp = Path(tempfile.gettempdir()) / "tts_tmp.mp3"
        tts.save(tmp)
        return tmp

