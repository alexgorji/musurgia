from pathlib import Path


def pytest_configure(config):
    import os

    fonts_dir = Path(__file__).parent / "fonts"
    os.environ["FONTCONFIG_FILE"] = str(fonts_dir / "fonts.conf")
