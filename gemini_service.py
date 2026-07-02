"""Acceso aislado al SDK de Gemini."""

from typing import Any

from google import genai
from google.genai import types


class GeminiService:
    """Crea chats y consulta modelos sin depender de Streamlit."""

    def __init__(
        self,
        api_key: str,
        model: str,
        system_instruction: str,
        client: genai.Client | None = None,
    ) -> None:
        self._client = client or genai.Client(api_key=api_key)
        self._model = model
        self._system_instruction = system_instruction

    def new_chat(self) -> Any:
        """Inicia una conversación con las instrucciones configuradas."""
        return self._client.chats.create(
            model=self._model,
            config=types.GenerateContentConfig(
                system_instruction=self._system_instruction,
                temperature=0.2,
                max_output_tokens=1024,
            ),
        )

    def list_available_models(self) -> list[str]:
        """Devuelve los modelos capaces de generar contenido."""
        return [
            model.name
            for model in self._client.models.list()
            if getattr(model, "supported_actions", None)
            and "generateContent" in model.supported_actions
        ]


def content_text(content: Any) -> str:
    """Extrae el texto de todas las partes de una respuesta del SDK."""
    return "".join(
        getattr(part, "text", "") or "" for part in getattr(content, "parts", [])
    )


def response_text(response: Any) -> str:
    """Valida y normaliza el texto devuelto por el modelo."""
    text = (getattr(response, "text", None) or "").strip()
    if not text:
        raise ValueError("El modelo devolvió una respuesta vacía.")
    return text
