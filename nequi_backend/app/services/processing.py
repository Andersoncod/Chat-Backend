from datetime import datetime
from typing import Tuple
from app.core.config import settings


# procesamiento de funciones

def filter_inappropriate(content: str) -> Tuple[bool, str]:
    """
    Retorna (is_clean, filtered_content). Si encuentra palabras prohibidas, las enmascara.
    """
    tokens = content.split()
    banned = settings.BANNED_WORDS
    clean = True
    filtered = []
    for t in tokens:
        if t.lower() in banned:
            clean = False
            filtered.append("*" * len(t))
        else:
            filtered.append(t)
    return clean, " ".join(filtered)

def build_metadata(content: str) -> dict:
    words = [w for w in content.split() if w.strip()]
    return {
        "word_count": len(words),
        "character_count": len(content),
        "processed_at": datetime.utcnow().isoformat() + "Z",
    }
