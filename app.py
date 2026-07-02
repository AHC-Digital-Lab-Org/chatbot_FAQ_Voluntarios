import logging

import streamlit as st
from google.genai.errors import APIError
from streamlit.errors import StreamlitSecretNotFoundError

from chat_logic import MAX_PROMPT_CHARS, error_details, normalize_prompt
from config import BOT_AVATAR_PATH, DEFAULT_GEMINI_MODEL, load_system_prompt
from gemini_service import GeminiService, content_text, response_text
from ui import (
    configure_page,
    render_error,
    render_footer,
    render_header,
    render_sidebar,
    render_welcome,
)

LOGGER = logging.getLogger(__name__)
configure_page()  # Debe ser la primera llamada de Streamlit.

# ── Constantes de marca AHC ────────────────────────────────────────────────────


def _get_secret(name: str) -> str | None:
    """Lee un secreto de Streamlit sin reventar si aún no se ha configurado."""
    try:
        value = st.secrets.get(name)
    except StreamlitSecretNotFoundError:
        return None
    return str(value) if value else None


# El administrador puede sobrescribir el modelo mediante Streamlit Secrets.
GEMINI_MODEL = _get_secret("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL

# ── Configuración Streamlit ────────────────────────────────────────────────────

# ── Cliente Gemini ──────────────────────────────────────────────────────────────


@st.cache_resource
def get_gemini_service(api_key: str, model: str) -> GeminiService:
    return GeminiService(
        api_key=api_key,
        model=model,
        system_instruction=load_system_prompt(),
    )


# ── Estilo personalizado AHC ───────────────────────────────────────────────────

render_header()

# ── Cabecera con logo AHC ──────────────────────────────────────────────────────

# ── Estado de sesión ────────────────────────────────────────────────────────────

# Si el administrador todavía no ha cargado la clave de la API en Streamlit Cloud,
# mostramos un aviso en lugar de que la app termine con un error genérico.
api_key = _get_secret("GEMINI_API_KEY")
if render_sidebar(api_configured=api_key is not None):
    st.session_state.pop("chat", None)
    st.rerun()

if api_key is None:
    st.info(
        "⏳ **El asistente está casi listo.**\n\n"
        "La persona administradora debe completar la configuración del servicio."
    )
    st.stop()

if "chat" not in st.session_state:
    try:
        st.session_state.chat = get_gemini_service(api_key, GEMINI_MODEL).new_chat()
    except Exception:
        LOGGER.exception("No se pudo inicializar el cliente de Gemini")
        st.error(
            "No se pudo iniciar el asistente. Contacta con la persona "
            "administradora para revisar la configuración."
        )
        st.stop()

# ── Historial de chat ──────────────────────────────────────────────────────────


history = st.session_state.chat.get_history()
if not history:
    render_welcome()

for content in history:
    role = "user" if content.role == "user" else "assistant"
    avatar = BOT_AVATAR_PATH if role == "assistant" else None
    with st.chat_message(role, avatar=avatar):
        st.markdown(content_text(content))

# ── Captura nueva pregunta ─────────────────────────────────────────────────────

if prompt := st.chat_input(
    "Escribe tu duda sobre la AHC...",
    max_chars=MAX_PROMPT_CHARS,
):
    try:
        prompt = normalize_prompt(prompt)
    except ValueError as error:
        st.warning(str(error))
        st.stop()

    with st.chat_message("user"):
        st.markdown(prompt)

    with (
        st.chat_message("assistant", avatar=BOT_AVATAR_PATH),
        st.spinner("Pensando..."),
    ):
        try:
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response_text(response))
        except APIError as error:
            LOGGER.warning("Gemini rechazó una consulta", exc_info=True)
            render_error(error_details(error))
        except ValueError:
            LOGGER.warning("Gemini devolvió una respuesta vacía", exc_info=True)
            st.error("No he recibido una respuesta válida. Inténtalo de nuevo.")
        except Exception:
            LOGGER.exception("Fallo inesperado al consultar Gemini")
            st.error("Se produjo un error inesperado. Inténtalo de nuevo más tarde.")

# ── Footer ─────────────────────────────────────────────────────────────────────

render_footer()
