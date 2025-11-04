from __future__ import annotations
from typing import Optional
from gtts import gTTS
from io import BytesIO

def synthesize_speech_to_bytes(text: str, lang: str = "pl") -> Optional[bytes]:
    try:
        lang_code = "pl" if lang == "pl" else "en"
        tts = gTTS(text=text, lang=lang_code)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception:
        return None
