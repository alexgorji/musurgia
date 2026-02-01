from pathlib import Path
from musurgia.tests.helpers.svg import SVGTestCase

path = Path(__file__).parent


class TestSVGTestCase(SVGTestCase):
    def test_compare(self):
        self.compareSVGToPNG(
            svg_path=path / "test.svg", png_path=path / "golden.png"
        )
