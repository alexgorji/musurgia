from pathlib import Path

from musurgia.fractaltree.fractalmusic import FractalMusic
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase, create_path

path = Path(__file__)


class Test(TestCase):
    def setUp(self):
        self.pdf = Pdf()
        self.fm = FractalMusic(duration=10)
        self.fm.add_layer()

    def test_draw_one_layer(self):
        self.pdf.write(create_path(path, 'draw_one_layer.pdf'))
        sl = self.fm.create_segmented_line_group()
        sl.draw(self.pdf)

        self.assertFalse(True)
