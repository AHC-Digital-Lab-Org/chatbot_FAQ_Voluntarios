import pathlib

import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# ── Constantes de marca AHC ────────────────────────────────────────────────────

BASE_DIR = pathlib.Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

AHC_GREEN = "#4F9447"
AHC_TITLE_GREEN = "#537358"
AHC_TEXT = "#222A1A"
AHC_LINK = "#A5C6A4"
AHC_BG_LIGHT = "#F4F1E9"

FAVICON_PATH = str(ASSETS_DIR / "favicon-192.png")
BOT_AVATAR_PATH = str(ASSETS_DIR / "favicon-192.png")

def _inline_svg(path: pathlib.Path) -> str:
    """Lee un SVG y prepara su markup para inyectarlo dentro de HTML.

    Streamlit/Markdown rompe el HTML siguiente si la cadena contiene
    una declaración XML (`<?xml ...?>`); también quitamos los saltos
    de línea iniciales para que no se interpreten como párrafo.
    """
    raw = path.read_text(encoding="utf-8")
    if raw.startswith("<?xml"):
        raw = raw.split("?>", 1)[1]
    return raw.strip()

LOGO_SVG = _inline_svg(ASSETS_DIR / "logo_ahc.svg")

GEMINI_MODEL = "gemini-3.1-flash-lite"

# ── Configuración Streamlit ────────────────────────────────────────────────────

st.set_page_config(
    page_title="Asistente AHC para Voluntarios",
    page_icon=FAVICON_PATH,
    layout="centered",
)

# ── Cliente Gemini ──────────────────────────────────────────────────────────────

@st.cache_resource
def get_client() -> genai.Client:
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


@st.cache_resource
def load_system_prompt() -> str:
    return (BASE_DIR / "system_prompt.md").read_text(encoding="utf-8")


def new_chat_session():
    return get_client().chats.create(
        model=GEMINI_MODEL,
        config=types.GenerateContentConfig(
            system_instruction=load_system_prompt(),
        ),
    )


def list_available_models() -> list[str]:
    """Modelos disponibles con tu API key. Útil para depurar 404."""
    return [
        m.name
        for m in get_client().models.list()
        if m.supported_actions and "generateContent" in m.supported_actions
    ]


# ── Estilo personalizado AHC ───────────────────────────────────────────────────

st.markdown(
    f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600&family=Source+Sans+3:wght@600;700&display=swap');

        html, body {{
            font-family: 'Nunito Sans', sans-serif;
            color: {AHC_TEXT};
        }}

        .stApp h1, .stApp h2, .stApp h3 {{
            font-family: 'Source Sans 3', sans-serif;
            color: {AHC_TITLE_GREEN};
        }}

        .stChatInput textarea {{
            border-color: {AHC_GREEN} !important;
        }}

        .stApp a {{
            color: {AHC_GREEN};
        }}

        .ahc-header {{
            display: flex;
            align-items: center;
            gap: 20px;
            padding: 12px 0 20px 0;
            border-bottom: 2px solid {AHC_GREEN};
            margin-bottom: 20px;
        }}

        .ahc-header svg {{
            width: 240px;
            max-width: 40%;
            height: auto;
            flex-shrink: 0;
        }}

        .ahc-header .ahc-title-block .ahc-title {{
            margin: 0;
            font-family: 'Source Sans 3', sans-serif;
            font-weight: 700;
            font-size: 22px;
            line-height: 1.2;
            color: {AHC_TITLE_GREEN};
        }}

        .ahc-header .ahc-title-block .ahc-tagline {{
            margin: 4px 0 0 0;
            font-size: 13px;
            color: {AHC_TEXT};
            opacity: 0.7;
        }}

        /* Reserva espacio al final para que el footer no quede tapado
           por el st.chat_input (position: fixed). */
        .ahc-footer {{
            margin: 32px 0 120px 0;
            padding-top: 16px;
            border-top: 1px solid {AHC_LINK};
            text-align: center;
            font-size: 12px;
            color: {AHC_TEXT};
            opacity: 0.6;
        }}

        .ahc-footer a {{
            color: {AHC_GREEN};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Cabecera con logo AHC ──────────────────────────────────────────────────────

st.markdown(
    f'<div class="ahc-header">{LOGO_SVG}'
    '<div class="ahc-title-block">'
    '<div class="ahc-title">Asistente para Voluntarios</div>'
    '<div class="ahc-tagline">Resuelvo dudas sobre el Campus, EcoGestos '
    "y procedimientos de la AHC</div>"
    "</div></div>",
    unsafe_allow_html=True,
)

# ── Estado de sesión ────────────────────────────────────────────────────────────

if "chat" not in st.session_state:
    st.session_state.chat = new_chat_session()

# ── Historial de chat ──────────────────────────────────────────────────────────


def _content_text(content) -> str:
    """Extrae el texto plano de un Content del SDK (parts puede tener varios)."""
    return "".join(getattr(part, "text", "") or "" for part in content.parts)


for content in st.session_state.chat.get_history():
    role = "user" if content.role == "user" else "assistant"
    avatar = BOT_AVATAR_PATH if role == "assistant" else None
    with st.chat_message(role, avatar=avatar):
        st.markdown(_content_text(content))

# ── Captura nueva pregunta ─────────────────────────────────────────────────────

if prompt := st.chat_input("Escribe tu duda aquí..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR_PATH):
        with st.spinner("Pensando..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
            except APIError as e:
                status = getattr(e, "code", None) or getattr(e, "status_code", None)
                if status == 429:
                    st.warning(
                        "Estoy procesando demasiadas consultas en este momento "
                        "(límite de la capa gratuita de Gemini: 15 peticiones/minuto). "
                        "Por favor, inténtalo de nuevo en 1 minuto."
                    )
                elif status == 403:
                    st.error(
                        "La API de Google ha rechazado la petición "
                        "(`403 PERMISSION_DENIED`). El proyecto Google asociado a la API key "
                        "está bloqueado. Crea una API key nueva en un proyecto nuevo en "
                        "https://aistudio.google.com/apikey y actualiza "
                        "`.streamlit/secrets.toml`."
                    )
                    try:
                        st.caption("Modelos disponibles con tu key actual:")
                        st.code("\n".join(list_available_models()) or "ninguno")
                    except Exception as e2:
                        st.code(f"No se pudo listar modelos: {e2}")
                else:
                    st.error(
                        f"Error de la API de Gemini al consultar `{GEMINI_MODEL}`:\n\n"
                        f"```\n{e}\n```"
                    )
            except Exception as e:
                st.error(f"Error inesperado:\n\n```\n{e}\n```")

# ── Footer ─────────────────────────────────────────────────────────────────────

st.markdown(
    '<div class="ahc-footer">'
    "Para consultas no cubiertas: "
    '<a href="mailto:secretaria@asociacionhuelladecarbono.org">'
    "secretaria@asociacionhuelladecarbono.org</a>"
    "</div>",
    unsafe_allow_html=True,
)
