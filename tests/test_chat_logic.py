from types import SimpleNamespace

import pytest

from chat_logic import MAX_PROMPT_CHARS, error_details, normalize_prompt


def test_normalize_prompt_trims_surrounding_whitespace() -> None:
    assert normalize_prompt("  ¿Cómo accedo al Campus?  ") == "¿Cómo accedo al Campus?"


@pytest.mark.parametrize("prompt", ["", "   ", "\n\t"])
def test_normalize_prompt_rejects_empty_text(prompt: str) -> None:
    with pytest.raises(ValueError, match="Escribe una pregunta"):
        normalize_prompt(prompt)


def test_normalize_prompt_rejects_oversized_text() -> None:
    with pytest.raises(ValueError, match=f"{MAX_PROMPT_CHARS}"):
        normalize_prompt("a" * (MAX_PROMPT_CHARS + 1))


@pytest.mark.parametrize(
    ("status", "level", "expected_text"),
    [
        (429, "warning", "unos instantes"),
        (401, "error", "configuración"),
        (403, "error", "configuración"),
        (404, "error", "modelo"),
        (503, "error", "temporalmente"),
        (None, "error", "procesar"),
    ],
)
def test_error_details_returns_safe_actionable_messages(
    status: int | None,
    level: str,
    expected_text: str,
) -> None:
    error = SimpleNamespace(code=status)

    details = error_details(error)

    assert details.level == level
    assert expected_text in details.message
    assert "API key" not in details.message


def test_error_details_reads_status_code_fallback() -> None:
    details = error_details(SimpleNamespace(status_code=429))

    assert details.level == "warning"
