from fractions import Fraction
from math import ceil, floor
from unittest import TestCase


from musicscore import Metronome
from musurgia.timing.duration import (
    Duration,
    convert_duration_to_quarter_duration_value,
    convert_quarter_duration_to_duration_value,
)


class TestDuration(TestCase):
    def test_seconds(self):
        d = Duration(seconds=10)
        assert d.seconds == 10
        assert d.minutes == 0
        assert d.hours == 0
        assert d.get_clock_as_string() == "0:00:10.0"

    def test_seconds_over_60(self):
        d = Duration(seconds=70)
        assert d.seconds == 10
        assert d.minutes == 1
        assert d.hours == 0
        assert d.get_clock_as_string() == "0:01:10.0"

    def test_seconds_over_3600(self):
        d = Duration(seconds=3610)
        assert d.seconds == 10
        assert d.minutes == 0
        assert d.hours == 1
        assert d.get_clock_as_string() == "1:00:10.0"

    def test_seconds_float(self):
        d = Duration(seconds=10.5)
        assert d.get_clock_as_string() == "0:00:10.5"

    def test_minutes(self):
        d = Duration(minutes=10)
        assert d.seconds == 0
        assert d.minutes == 10
        assert d.hours == 0
        assert d.get_clock_as_string() == "0:10:00.0"

    def test_minutes_over_60(self):
        d = Duration(minutes=75)
        assert d.seconds == 0
        assert d.minutes == 15
        assert d.hours == 1
        assert d.get_clock_as_string() == "1:15:00.0"

    def test_minutes_float(self):
        d = Duration(minutes=10.5)
        assert d.get_clock_as_string() == "0:10:30.0"

    def test_hours(self):
        d = Duration(hours=3)
        assert d.seconds == 0
        assert d.minutes == 0
        assert d.hours == 3
        assert d.get_clock_as_string() == "3:00:00.0"

    def test_no_arguments(self):
        d = Duration()
        assert d.seconds == 0
        assert d.minutes == 0
        assert d.hours == 0
        assert d.get_clock_as_string() == "0:00:00.0"

    def test_complex_input(self):
        d = Duration(hours=2.5, minutes=70.5, seconds=70.5)
        assert d.get_clock_as_string() == "3:41:40.5"

    def test_get_clock_modes(self):
        d = Duration(hours=2.5, minutes=90.5, seconds=90.5)
        assert d.get_clock_as_string(mode="hms") == "4:02:00.5"
        assert d.get_clock_as_string(mode="ms") == "02:00.5"
        assert d.get_clock_as_string(mode="msreduced") == "2:0.5"

    def test_calculate_in_seconds(self):
        d = Duration(hours=1, minutes=30, seconds=30)
        assert d.calculate_in_seconds() == 5430.0

    def test_calculate_in_minutes(self):
        d = Duration(hours=1, minutes=30, seconds=30)
        assert d.calculate_in_minutes() == 90.5

    def test_calculate_in_hours(self):
        d = Duration(hours=1, minutes=30, seconds=30)
        assert float(d.calculate_in_hours()) == 1.5083333333333333

    def test_set_and_get_values(self):
        d = Duration(hours=1, minutes=30, seconds=30)
        assert d.clock.get_values() == (1, 30, 30)
        d.hours = 2
        assert d.clock.get_values() == (2, 30, 30)
        d.minutes = 10
        assert d.clock.get_values() == (2, 10, 30)
        d.seconds = 20.0
        assert d.clock.get_values() == (2, 10, 20)
        d.minutes = 65
        assert d.clock.get_values() == (3, 5, 20)

    def test_fractioned_clock(self):
        d = Duration(Fraction(10, 3))
        assert d.seconds == Fraction(10, 3)


# class TestConvertors(TestCase):
#     def test_convert_duration_to_quarter_duration(self):
#         t = 60
#         d = Duration(seconds=3)
#         assert convert_duration_to_quarter_duration_value(d, t) == 3
#         t = 30
#         assert convert_duration_to_quarter_duration_value(d, t) == QuarterDuration(1.5)
#         assert convert_duration_to_quarter_duration_value(3, 120) == 6
#         t = Metronome(60, 2)
#         assert convert_duration_to_quarter_duration_value(3, t) == 6

#     import unittest


class QuarterDurationConversionTestCase(TestCase):
    def test_basic_case(self):
        # Test case 1: 60 quarters per minute, 60 seconds duration
        metronome = Metronome(per_minute=60, beat_unit=1)  # 60 quarters per minute
        duration = 60  # 60 seconds
        self.assertEqual(
            convert_duration_to_quarter_duration_value(metronome, duration), 60
        )

    def test_half_quarters(self):
        # Test case 2: 120 quarters per minute, 30 seconds duration
        metronome = Metronome(per_minute=120, beat_unit=1)  # 120 quarters per minute
        duration = 30  # 30 seconds
        self.assertEqual(
            convert_duration_to_quarter_duration_value(metronome, duration), 60
        )

    def test_triplet_quarters(self):
        # Test case 3: 90 quarters per minute, 20 seconds duration
        metronome = Metronome(per_minute=90, beat_unit=1)  # 90 quarters per minute
        duration = 20  # 20 seconds
        self.assertEqual(
            convert_duration_to_quarter_duration_value(metronome, duration), 30
        )

    def test_fractional_duration(self):
        # Test case 4: 120 quarters per minute, 2.5 seconds duration
        metronome = Metronome(per_minute=120, beat_unit=1)  # 120 quarters per minute
        duration = 2.5  # 2.5 seconds
        self.assertEqual(
            convert_duration_to_quarter_duration_value(metronome, duration), 5
        )

    def test_zero_duration(self):
        # Test case 5: 120 quarters per minute, 0 seconds duration
        metronome = Metronome(per_minute=120, beat_unit=1)  # 120 quarters per minute
        duration = 0  # 0 seconds
        self.assertEqual(
            convert_duration_to_quarter_duration_value(metronome, duration), 0
        )

    def test_high_bpm_short_duration(self):
        # Test case 6: 240 quarters per minute, 0.5 seconds duration
        metronome = Metronome(per_minute=240, beat_unit=1)  # 240 quarters per minute
        duration = 0.5  # 0.5 seconds
        self.assertEqual(
            convert_duration_to_quarter_duration_value(metronome, duration), 2
        )

    def test_low_bpm_long_duration(self):
        # Test case 7: 30 quarters per minute, 120 seconds duration
        metronome = Metronome(per_minute=30, beat_unit=1)  # 30 quarters per minute
        duration = 120  # 120 seconds
        self.assertEqual(
            convert_duration_to_quarter_duration_value(metronome, duration), 60
        )

    def test_edge_case_small_bpm(self):
        # Test case 8: 15 quarters per minute, 60 seconds duration
        metronome = Metronome(per_minute=15, beat_unit=1)  # 15 quarters per minute
        duration = 60  # 60 seconds
        self.assertEqual(
            convert_duration_to_quarter_duration_value(metronome, duration), 15
        )

    def test_edge_case_large_bpm(self):
        # Test case 9: 480 quarters per minute, 1 second duration
        metronome = Metronome(per_minute=480, beat_unit=1)  # 480 quarters per minute
        duration = 1  # 1 second
        self.assertEqual(
            convert_duration_to_quarter_duration_value(metronome, duration), 8
        )

    def test_exact_quarter_duration(self):
        # Test case 10: 60 quarters per minute, 1 second duration
        metronome = Metronome(per_minute=60, beat_unit=1)  # 60 quarters per minute
        duration = 1  # 1 second
        self.assertEqual(
            convert_duration_to_quarter_duration_value(metronome, duration), 1
        )


class DurationToQuarterDurationConversionTestCase(TestCase):
    def test_basic_case(self):
        # Test case 1: Convert 60 quarters to seconds with metronome 120 BPM and beat unit 1 (quarter note per beat)
        metronome = Metronome(per_minute=120, beat_unit=1)
        quarter_duration = 60  # 60 quarters
        self.assertEqual(
            convert_quarter_duration_to_duration_value(metronome, quarter_duration), 30
        )

    def test_half_note_case(self):
        # Test case 2: Convert 60 quarters to seconds with metronome 120 BPM and beat unit 2 (half note per beat)
        metronome = Metronome(
            per_minute=120, beat_unit=2
        )  # 2 quarters per beat (half note)
        quarter_duration = 60  # 60 quarters
        self.assertEqual(
            convert_quarter_duration_to_duration_value(metronome, quarter_duration), 15
        )

    def test_eighth_note_case(self):
        # Test case 3: Convert 15 quarters to seconds with metronome 90 BPM and beat unit 0.5 (eighth note per beat)
        metronome = Metronome(
            per_minute=90, beat_unit=0.5
        )  # 0.5 quarters per beat (eighth note)
        quarter_duration = 15  # 15 quarters
        self.assertEqual(
            convert_quarter_duration_to_duration_value(metronome, quarter_duration), 20
        )

    def test_zero_quarter_duration(self):
        # Test case 4: Convert 0 quarters to seconds (edge case)
        metronome = Metronome(per_minute=120, beat_unit=1)  # 1 quarter per beat
        quarter_duration = 0  # 0 quarters
        self.assertEqual(
            convert_quarter_duration_to_duration_value(metronome, quarter_duration), 0
        )

    def test_fractional_quarters(self):
        # Test case 5: Convert 5 quarters to seconds with metronome 60 BPM and beat unit 0.5 (eighth note per beat)
        metronome = Metronome(
            per_minute=60, beat_unit=0.5
        )  # 0.5 quarters per beat (eighth note)
        quarter_duration = 5  # 5 quarters
        self.assertEqual(
            convert_quarter_duration_to_duration_value(metronome, quarter_duration), 10
        )

    def test_large_bpm_case(self):
        # Test case 6: Convert 120 quarters to seconds with metronome 240 BPM and beat unit 1 (quarter note per beat)
        metronome = Metronome(per_minute=240, beat_unit=1)  # 1 quarter per beat
        quarter_duration = 120  # 120 quarters
        self.assertEqual(
            convert_quarter_duration_to_duration_value(metronome, quarter_duration), 30
        )

    def test_small_bpm_case(self):
        # Test case 7: Convert 10 quarters to seconds with metronome 30 BPM and beat unit 1 (quarter note per beat)
        metronome = Metronome(per_minute=30, beat_unit=1)  # 1 quarter per beat
        quarter_duration = 10  # 10 quarters
        self.assertEqual(
            convert_quarter_duration_to_duration_value(metronome, quarter_duration), 20
        )

    def test_large_quarter_duration(self):
        # Test case 8: Convert 500 quarters to seconds with metronome 60 BPM and beat unit 1 (quarter note per beat)
        metronome = Metronome(per_minute=60, beat_unit=1)  # 1 quarter per beat
        quarter_duration = 500  # 500 quarters
        self.assertEqual(
            convert_quarter_duration_to_duration_value(metronome, quarter_duration), 500
        )

    def test_fractional_bpm_case(self):
        # Test case 9: Convert 40 quarters to seconds with metronome 75 BPM and beat unit 1 (quarter note per beat)
        metronome = Metronome(per_minute=75, beat_unit=1)  # 1 quarter per beat
        quarter_duration = 40  # 40 quarters
        self.assertEqual(
            convert_quarter_duration_to_duration_value(metronome, quarter_duration), 32
        )

    def test_edge_case_high_beat_unit(self):
        # Test case 10: Convert 10 quarters to seconds with metronome 120 BPM and beat unit 2 (half note per beat)
        metronome = Metronome(
            per_minute=120, beat_unit=2
        )  # 2 quarters per beat (half note)
        quarter_duration = 10  # 10 quarters
        self.assertEqual(
            convert_quarter_duration_to_duration_value(metronome, quarter_duration), 2.5
        )


class TestMagics(TestCase):
    cl = Duration

    def setUp(self):
        self.main = self.cl(70)
        self.equal = self.cl(70)
        self.equal_float = 70.0
        self.larger = self.cl(80)
        self.larger_float = 80.0
        self.smaller = self.cl(60)
        self.smaller_float = 60.0

    def test_abs(self):
        assert abs(self.cl(-70)).calculate_in_seconds() == 70

    def test_ceil(self):
        assert ceil(self.cl(70.2)).calculate_in_seconds() == 71

    def test_floor(self):
        assert floor(self.cl(70.2)).calculate_in_seconds() == 70

    def test_floor_division(self):
        a = self.cl(10)
        b = self.cl(4)
        c = self.cl(2)
        assert a // b == c
        assert a // 4 == c
        assert a // b == 2
        assert a // 4 == 2

    def test_gt(self):
        assert self.main > self.smaller
        assert self.main > self.smaller_float
        assert not self.main > self.equal
        assert not self.main > self.equal_float
        assert not self.main > self.larger
        assert not self.main > self.larger_float

    def test_ge(self):
        assert self.main >= self.smaller
        assert self.main >= self.smaller_float
        assert self.main >= self.equal
        assert self.main >= self.equal_float
        assert not self.main >= self.larger
        assert not self.main >= self.larger_float

    def test_le(self):
        assert not self.main <= self.smaller
        assert not self.main <= self.smaller_float
        assert self.main <= self.equal
        assert self.main <= self.equal_float
        assert self.main <= self.larger
        assert self.main <= self.larger_float

    def test_lt(self):
        assert not self.main < self.smaller
        assert not self.main < self.smaller_float
        assert not self.main < self.equal
        assert not self.main < self.equal_float
        assert self.main < self.larger
        assert self.main < self.larger_float

    def test_mod(self):
        a = self.cl(10)
        b = self.cl(3)
        c = self.cl(1)
        assert a % 3 == c
        assert a % 3 == 1
        assert a % b == c
        assert a % b == 1

    def test_mul(self):
        a = self.cl(10)
        b = self.cl(3)
        c = self.cl(30)
        assert a * b == 30
        assert a * b == c
        assert a * 3 == 30
        assert a * 3 == c

    def test_neg(self):
        a = self.cl(10)
        b = self.cl(-10)
        assert -a == b
        assert -a == -10
        assert -b == a
        assert -b == 10

    def test_pos(self):
        a = self.cl(10)
        assert +a == a

    def test_power(self):
        a = self.cl(10)
        b = self.cl(100)
        assert 10.0**2 == 100
        assert a**2 == 100
        assert a**2 == b

    def test_radd(self):
        a = self.cl(10)
        b = self.cl(100)
        assert a.__radd__(b) == b + a

    def test_rmod(self):
        a = self.cl(3)
        b = self.cl(10)
        assert a.__rmod__(b) == b % a

    def test_rmul(self):
        a = self.cl(3)
        b = self.cl(10)
        assert a.__rmul__(b) == b * a

    def test_eq(self):
        a = self.cl(10)
        b = self.cl(10)
        c = self.cl(11)
        assert a == b
        assert a == 10
        assert 10 == a
        assert a == 10.0
        assert a != 11
        assert a != c
        assert not a == c
        assert not a == 11
        assert not 11 == a
        d = self.cl(Fraction(10, 3))
        assert Fraction(10, 3) == Fraction(10, 3)
        assert Fraction(10, 3).__eq__(Fraction(10, 3))
        assert d.__eq__(Fraction(10, 3))
        assert d == Fraction(10, 3)
        assert a is not None

    def test_round(self):
        assert self.cl(70.7) == self.cl(70.7)
        assert round(self.cl(70.67), 1) == 70.7
        assert round(self.cl(70.67), 1) == self.cl(70.7)
        assert round(self.cl(70.67), 1) != self.cl(70.6)
        assert round(self.cl(70.67), 1) != 70.6

    def test_rtruediv(self):
        a = self.cl(3)
        b = self.cl(10)
        assert a.__rtruediv__(b) == Fraction(10, 3)

    def test_truediv(self):
        a = self.cl(10)
        b = self.cl(3)
        assert a / b == Fraction(10, 3)

    def test_trunc(self):
        a = self.cl(10.233)
        assert a.__trunc__() == 10

    def test_rfloordiv(self):
        a = self.cl(3)
        b = self.cl(10)
        assert a.__rfloordiv__(b) == b // a
