from types import SimpleNamespace
from typing import Any

import pytest

from gemini_service import GeminiService, content_text, response_text


class FakeChats:
    def __init__(self) -> None:
        self.arguments: dict[str, Any] = {}

    def create(self, **kwargs: Any) -> str:
        self.arguments = kwargs
        return "chat"


class FakeModels:
    def list(self) -> list[SimpleNamespace]:
        return [
            SimpleNamespace(
                name="models/gemini-test",
                supported_actions=["generateContent"],
            ),
            SimpleNamespace(
                name="models/embed-test", supported_actions=["embedContent"]
            ),
        ]


def make_service() -> tuple[GeminiService, SimpleNamespace]:
    client = SimpleNamespace(chats=FakeChats(), models=FakeModels())
    service = GeminiService(
        api_key="unused",
        model="gemini-test",
        system_instruction="Responde con precisión.",
        client=client,
    )
    return service, client


def test_new_chat_uses_configured_model_and_prompt() -> None:
    service, client = make_service()

    assert service.new_chat() == "chat"
    assert client.chats.arguments["model"] == "gemini-test"
    config = client.chats.arguments["config"]
    assert config.system_instruction == "Responde con precisión."
    assert config.temperature == 0.2
    assert config.max_output_tokens == 1024


def test_list_available_models_filters_unsupported_actions() -> None:
    service, _ = make_service()

    assert service.list_available_models() == ["models/gemini-test"]


def test_content_text_joins_parts_and_ignores_missing_text() -> None:
    content = SimpleNamespace(
        parts=[
            SimpleNamespace(text="Hola"),
            SimpleNamespace(),
            SimpleNamespace(text=" mundo"),
        ]
    )

    assert content_text(content) == "Hola mundo"


def test_content_text_accepts_content_without_parts() -> None:
    assert content_text(SimpleNamespace()) == ""


def test_response_text_rejects_an_empty_model_response() -> None:
    with pytest.raises(ValueError, match="respuesta vacía"):
        response_text(SimpleNamespace(text="  "))


def test_response_text_returns_trimmed_model_response() -> None:
    assert (
        response_text(SimpleNamespace(text="  Respuesta segura.  "))
        == "Respuesta segura."
    )
