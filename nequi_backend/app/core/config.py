import os

class Settings:
    SQLITE_URL: str = os.getenv("SQLITE_URL", "sqlite:///./messages.db")
    # Palabras prohibidas simples (demo). En real, se cargaría de config/DB
    BANNED_WORDS: set[str] = {"insulto", "grosería", "inapropiado"}

settings = Settings()
