"""Reglas puras de entrada y presentación de errores del chat."""

from dataclasses import dataclass
from typing import Any, Literal

MAX_PROMPT_CHARS = 2_000


@dataclass(frozen=True)
class ErrorDetails:
    """Mensaje seguro y nivel visual para un fallo del proveedor."""

    level: Literal["error", "warning"]
    message: str


def normalize_prompt(prompt: str) -> str:
    """Limpia y valida una pregunta antes de enviarla al modelo."""
    normalized = prompt.strip()
    if not normalized:
        raise ValueError("Escribe una pregunta antes de enviarla.")
    if len(normalized) > MAX_PROMPT_CHARS:
        raise ValueError(f"La pregunta no puede superar {MAX_PROMPT_CHARS} caracteres.")
    return normalized


def error_details(error: Any) -> ErrorDetails:
    """Traduce errores técnicos a mensajes accionables sin filtrar detalles."""
    status = getattr(error, "code", None) or getattr(error, "status_code", None)

    if status == 429:
        return ErrorDetails(
            "warning",
            "Hay muchas consultas en este momento. Espera unos instantes e "
            "inténtalo de nuevo.",
        )
    if status in {401, 403}:
        return ErrorDetails(
            "error",
            "El asistente necesita revisar la configuración del servicio. "
            "Contacta con la persona administradora.",
        )
    if status == 404:
        return ErrorDetails(
            "error",
            "El modelo configurado no está disponible. Contacta con la persona "
            "administradora.",
        )
    if isinstance(status, int) and status >= 500:
        return ErrorDetails(
            "error",
            "El servicio de respuestas no está disponible temporalmente. "
            "Inténtalo más tarde.",
        )
    return ErrorDetails(
        "error",
        "No he podido procesar la consulta. Inténtalo de nuevo o contacta con "
        "secretaría si el problema continúa.",
    )
