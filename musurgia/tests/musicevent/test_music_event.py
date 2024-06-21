from unittest import TestCase

from musicscore import Metronome

from musurgia.musicevent.musicevent import MusicEvent


class TestMusicEvent(TestCase):
    def setUp(self) -> None:
        from musicscore import QuarterDuration
        self.me = MusicEvent(midis=60, quarter_duration=QuarterDuration(3), tempo=Metronome(120))

    def test_fractal_music_duration(self):
        assert self.me.get_duration() == 1.5
        self.me.tempo.per_minute = 60
        assert self.me.get_duration() == 3
        self.me.quarter_duration = 6
        assert self.me.get_duration() == 6
