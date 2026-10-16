from pathlib import Path
from pytest import Config


def pytest_configure(config: Config) -> None:
    import os

    fonts_dir = Path(__file__).parent / "fonts"
    os.environ["FONTCONFIG_FILE"] = str(fonts_dir / "fonts.conf")
