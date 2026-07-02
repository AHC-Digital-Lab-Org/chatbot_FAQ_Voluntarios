"""Configuración y carga de recursos locales del chatbot."""

import base64
from pathlib import Path

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

DEFAULT_GEMINI_MODEL = "gemini-3.1-flash-lite"

FAVICON_PATH = str(ASSETS_DIR / "favicon-192.png")
BOT_AVATAR_PATH = str(ASSETS_DIR / "bot_avatar.png")
OFFICIAL_LOGO_PATH = ASSETS_DIR / "logo_ahc_oficial.jpg"


def load_text(path: Path) -> str:
    """Carga un recurso de texto UTF-8."""
    return path.read_text(encoding="utf-8")


def load_logo_svg() -> str:
    """Carga el logo sin la declaración XML que rompe Markdown."""
    raw = load_text(ASSETS_DIR / "logo_ahc.svg")
    if raw.startswith("<?xml"):
        raw = raw.split("?>", 1)[1]
    return raw.strip()


def load_official_logo_data_uri() -> str:
    """Codifica el logotipo oficial para incrustarlo sin depender de red."""
    encoded = base64.b64encode(OFFICIAL_LOGO_PATH.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def load_styles() -> str:
    """Carga la hoja de estilos de la interfaz."""
    return load_text(ASSETS_DIR / "styles.css")


def load_system_prompt() -> str:
    """Carga las instrucciones y la base de conocimiento del bot."""
    return load_text(BASE_DIR / "system_prompt.md")
