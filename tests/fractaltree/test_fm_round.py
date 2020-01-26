from unittest import TestCase

from musurgia.fractaltree.fractalmusic import FractalMusic


class Test(TestCase):
    def setUp(self) -> None:
        self.fm = FractalMusic(duration=10)

    def test_1(self):
        self.fm.tempo = 70
        print(self.fm.quarter_duration)
