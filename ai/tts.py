from __future__ import annotations
from typing import Optional, Tuple
from io import BytesIO

from gtts import gTTS


# gTTS nie lubi absurdalnie długich stringów – dobrze mieć bezpieczny limit
DEFAULT_MAX_CHARS = 5000


def _pick_lang_code(ui_lang: str) -> str:
    """
    Mapowanie języka z UI na kod gTTS.
    Jak chcesz więcej języków – dopisz je tutaj.
    """
    mapping = {
        "pl": "pl",
        "en": "en",
        "en-US": "en",
        "en-GB": "en",
    }
    return mapping.get(ui_lang, "en")


def synthesize_speech_to_bytes(
    text: str,
    lang: str = "pl",
    *,
    max_chars: int = DEFAULT_MAX_CHARS,
    slow: bool = False,
    tld: str = "com",
) -> Optional[bytes]:
    """
    Generuje MP3 w pamięci z użyciem gTTS.

    - przycina tekst jeśli jest za długi (żeby gTTS nie padło),
    - dobiera kod języka na podstawie języka UI,
    - umożliwia ustawienie wolniejszego czytania,
    - w razie błędu zwraca None (UI może wtedy pokazać komunikat).

    Uwaga: wymaga internetu w środowisku uruchomienia.
    """
    if not text or not text.strip():
        return None

    # przycinamy najdłuższe monologi ;)
    safe_text = text.strip()
    if len(safe_text) > max_chars:
        safe_text = safe_text[:max_chars] + "..."

    lang_code = _pick_lang_code(lang)

    try:
        tts = gTTS(text=safe_text, lang=lang_code, slow=slow, tld=tld)
        buf = BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()
    except Exception as exc:
        # tutaj można wpiąć logger, np. logging.exception(...)
        # żeby w Streamlicie pokazać "nie udało się wygenerować audio"
        return None
