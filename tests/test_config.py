from config import (
    ASSETS_DIR,
    OFFICIAL_LOGO_PATH,
    load_logo_svg,
    load_official_logo_data_uri,
    load_styles,
    load_system_prompt,
)


def test_required_resources_are_loaded() -> None:
    assert ASSETS_DIR.is_dir()
    assert load_system_prompt().strip()
    assert ".ahc-header" in load_styles()


def test_logo_is_safe_to_embed_in_markdown() -> None:
    logo = load_logo_svg()

    assert logo.startswith("<svg")
    assert "<?xml" not in logo


def test_official_logo_is_embedded_as_local_jpeg() -> None:
    assert OFFICIAL_LOGO_PATH.is_file()
    assert load_official_logo_data_uri().startswith("data:image/jpeg;base64,")
