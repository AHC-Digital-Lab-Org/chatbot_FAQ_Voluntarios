"""Componentes visuales de la aplicación Streamlit."""

import streamlit as st

from chat_logic import ErrorDetails
from config import (
    BOT_AVATAR_PATH,
    FAVICON_PATH,
    load_official_logo_data_uri,
    load_styles,
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
        '<h1 class="ahc-title">Asistente para voluntarios</h1>'
        '<p class="ahc-tagline">Campus, EcoGestos y procedimientos</p>'
        "</div>"
        '<div class="ahc-status"><span></span>Base AHC</div>'
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


def render_welcome() -> None:
    """Orienta al voluntario antes de su primera pregunta."""
    with st.chat_message("assistant", avatar=BOT_AVATAR_PATH):
        st.markdown(
            "Hola, soy el asistente para voluntarios de la AHC. Puedo ayudarte "
            "con información incluida en nuestra base interna."
        )
        st.markdown(
            '<div class="ahc-topics" aria-label="Temas disponibles">'
            "<span>Campus</span><span>EcoGestos</span><span>MITECO</span>"
            "<span>Voluntariado</span></div>",
            unsafe_allow_html=True,
        )
        st.caption("Prueba con: «¿Cómo recupero mi contraseña del Campus?»")


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
