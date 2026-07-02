from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_PATH = Path(__file__).parents[1] / "app.py"


def test_app_shows_safe_configuration_message_without_api_key() -> None:
    app = AppTest.from_file(str(APP_PATH))

    app.run(timeout=10)

    assert not app.exception
    assert any("casi listo" in message.value for message in app.info)
    assert not app.chat_input


def test_app_renders_welcome_and_chat_when_configured() -> None:
    app = AppTest.from_file(str(APP_PATH))
    app.secrets["GEMINI_API_KEY"] = "test-key"

    app.run(timeout=10)

    assert not app.exception
    assert len(app.chat_input) == 1
    assert app.chat_input[0].placeholder == "Escribe tu duda sobre la AHC..."
    assert len(app.chat_message) == 1
