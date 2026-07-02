"""Componentes visuales de la aplicación Streamlit."""

import streamlit as st

from chat_logic import ErrorDetails
from config import (
    BOT_AVATAR_PATH,
    FAVICON_PATH,
    load_official_logo_data_uri,
    load_styles,
)

SUGGESTED_PROMPTS = (
    ("Acceso al Campus", "He olvidado mi contraseña del Campus, ¿qué debo hacer?"),
    ("Qué es un EcoGesto", "¿Qué es un EcoGesto?"),
    ("Registro MITECO", "¿Cómo funciona el registro MITECO?"),
    ("Roles de voluntariado", "¿Qué roles de voluntariado existen en la AHC?"),
)


def configure_page() -> None:
    """Configura la página e instala los estilos AHC."""
    st.set_page_config(
        page_title="Asistente AHC para Voluntarios",
        page_icon=FAVICON_PATH,
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    st.markdown(f"<style>{load_styles()}</style>", unsafe_allow_html=True)


def render_header() -> None:
    """Muestra la identidad, alcance y estado del asistente."""
    st.markdown(
        '<header class="ahc-header">'
        f'<img class="ahc-logo" src="{load_official_logo_data_uri()}" '
        'alt="Asociación Huella de Carbono">'
        '<div class="ahc-title-block">'
        '<p class="ahc-eyebrow">Espacio de apoyo al voluntariado</p>'
        '<div class="ahc-title" role="heading" aria-level="1">'
        "Asistente para voluntarios</div>"
        '<p class="ahc-tagline">Campus, EcoGestos y procedimientos</p>'
        '<div class="ahc-status"><span></span>Base de conocimiento AHC</div>'
        "</div>"
        "</header>",
        unsafe_allow_html=True,
    )


def render_sidebar(api_configured: bool) -> bool:
    """Muestra controles y devuelve si se solicitó una conversación nueva."""
    with st.sidebar:
        st.markdown("## Asistente AHC")
        if api_configured:
            st.success("Servicio configurado")
        else:
            st.warning("Configuración pendiente")

        reset_requested = st.button(
            "Nueva conversación",
            use_container_width=True,
            disabled=not api_configured,
            type="primary",
            key="reset_chat_sidebar",
        )
        st.markdown("### Uso responsable")
        st.caption(
            "No compartas contraseñas, documentos de identidad, datos bancarios "
            "ni otra información sensible."
        )
        st.markdown(
            "Las consultas administrativas deben enviarse a "
            "[Secretaría](mailto:secretaria@asociacionhuelladecarbono.org)."
        )
    return reset_requested


def render_welcome() -> str | None:
    """Orienta al voluntario y devuelve una consulta sugerida si se pulsa."""
    with st.chat_message("assistant", avatar=BOT_AVATAR_PATH):
        st.markdown(
            "Hola, soy el asistente para voluntarios de la AHC. Puedo ayudarte "
            "con información incluida en nuestra base interna."
        )

    st.caption("Consultas frecuentes")
    columns = st.columns(2)
    for index, (label, prompt) in enumerate(SUGGESTED_PROMPTS):
        with columns[index % 2]:
            if st.button(label, key=f"suggestion_{index}", use_container_width=True):
                return prompt
    return None


def render_chat_toolbar(has_history: bool) -> bool:
    """Ofrece un reinicio visible cuando ya existe conversación."""
    if not has_history:
        return False

    _, action_column = st.columns([3, 1])
    with action_column:
        return st.button(
            "Nueva conversación",
            type="primary",
            use_container_width=True,
            key="reset_chat_main",
        )


def render_error(details: ErrorDetails) -> None:
    """Presenta un error ya traducido a lenguaje seguro."""
    if details.level == "warning":
        st.warning(details.message)
    else:
        st.error(details.message)


def render_footer() -> None:
    """Muestra contacto, privacidad y limitaciones del asistente."""
    st.markdown(
        '<footer class="ahc-footer">'
        "<strong>Asistente informativo AHC</strong> · Las respuestas se basan en "
        "la documentación interna disponible y pueden requerir confirmación. "
        '<a href="mailto:secretaria@asociacionhuelladecarbono.org">'
        "Contactar con Secretaría</a>"
        "</footer>",
        unsafe_allow_html=True,
    )
