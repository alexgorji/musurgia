from unittest import TestCase

from musicscore import QuarterDuration

from musicscore import Metronome
from musurgia.timing.duration import Duration, convert_duration_to_quarter_duration, \
    convert_quarter_duration_to_duration


class TestDuration(TestCase):
    def test_seconds(self):
        d = Duration(seconds=10)
        assert d.seconds == 10
        assert d.minutes == 0
        assert d.hours == 0
        assert d.get_clock_as_string() == '0:00:10.0'

    def test_seconds_over_60(self):
        d = Duration(seconds=70)
        assert d.seconds == 10
        assert d.minutes == 1
        assert d.hours == 0
        assert d.get_clock_as_string() == '0:01:10.0'

    def test_seconds_over_3600(self):
        d = Duration(seconds=3610)
        assert d.seconds == 10
        assert d.minutes == 0
        assert d.hours == 1
        assert d.get_clock_as_string() == '1:00:10.0'

    def test_seconds_float(self):
        d = Duration(seconds=10.5)
        assert d.get_clock_as_string() == '0:00:10.5'

    def test_minutes(self):
        d = Duration(minutes=10)
        assert d.seconds == 0
        assert d.minutes == 10
        assert d.hours == 0
        assert d.get_clock_as_string() == '0:10:00.0'

    def test_minutes_over_60(self):
        d = Duration(minutes=75)
        assert d.seconds == 0
        assert d.minutes == 15
        assert d.hours == 1
        assert d.get_clock_as_string() == '1:15:00.0'

    def test_minutes_float(self):
        d = Duration(minutes=10.5)
        assert d.get_clock_as_string() == '0:10:30.0'

    def test_hours(self):
        d = Duration(hours=3)
        assert d.seconds == 0
        assert d.minutes == 0
        assert d.hours == 3
        assert d.get_clock_as_string() == '3:00:00.0'

    def test_no_arguments(self):
        d = Duration()
        assert d.seconds == 0
        assert d.minutes == 0
        assert d.hours == 0
        assert d.get_clock_as_string() == '0:00:00.0'

    def test_complex_input(self):
        d = Duration(hours=2.5, minutes=70.5, seconds=70.5)
        assert d.get_clock_as_string() == '3:41:40.5'

    def test_get_clock_modes(self):
        d = Duration(hours=2.5, minutes=90.5, seconds=90.5)
        assert d.get_clock_as_string(mode='hms') == '4:02:00.5'
        assert d.get_clock_as_string(mode='ms') == '02:00.5'
        assert d.get_clock_as_string(mode='msreduced') == '2:0.5'

    def test_calculate_in_seconds(self):
        d = Duration(hours=1, minutes=30, seconds=30)
        assert d.calculate_in_seconds() == 5430.0

    def test_calculate_in_minutes(self):
        d = Duration(hours=1, minutes=30, seconds=30)
        assert d.calculate_in_minutes() == 90.5

    def test_calculate_in_hours(self):
        d = Duration(hours=1, minutes=30, seconds=30)
        assert d.calculate_in_hours() == 1.5083333333333333

    def test_convert_duration_to_quarter_duration(self):
        t = 60
        d = Duration(seconds=3)
        assert convert_duration_to_quarter_duration(d, t) == 3
        t = 30
        assert convert_duration_to_quarter_duration(d, t) == QuarterDuration(6)
        assert convert_duration_to_quarter_duration(3, 120) == 1.5
        t = Metronome(60, 2)
        assert convert_duration_to_quarter_duration(3, t) == 1.5

    def test_convert_quarter_duration_to_duration(self):
        qd = QuarterDuration(2)
        t = 60
        assert convert_quarter_duration_to_duration(qd, t) == Duration(seconds=2) == 2
        t = 120
        assert convert_quarter_duration_to_duration(qd, t) == Duration(seconds=1) == 1
