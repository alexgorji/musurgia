from unittest import TestCase

from musurgia.musicevent.musicevent import MusicEvent


class TestMusicEvent(TestCase):
    def setUp(self) -> None:
        from musicscore import QuarterDuration
        self.me = MusicEvent(quarter_duration=QuarterDuration(3), tempo=120)

    def test_fractal_music_duration(self):
        assert self.me.get_duration() == 1.5
        self.me.tempo = 60
        assert self.me.get_duration() == 3
        self.me.quarter_duration = 6
        assert self.me.get_duration() == 6

