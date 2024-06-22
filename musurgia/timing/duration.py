from fractions import Fraction
from typing import Any, Optional, Union

from musicscore import QuarterDuration, Metronome
from musurgia.musurgia_types import ConvertibleToFloat, check_type, ClockMode
from musurgia.timing.clock import Clock


def _convert_other(other):
    if isinstance(other, Duration):
        return other.calculate_in_seconds()

    return float(other)


class Duration:
    def __init__(self, seconds: ConvertibleToFloat = 0, minutes: ConvertibleToFloat = 0, hours: ConvertibleToFloat = 0,
                 *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._seconds: float = 0.0
        self._minutes: int = 0
        self._hours: int = 0
        self._clock: Clock
        self._set_clock(seconds=seconds, minutes=minutes, hours=hours)

    def _set_clock(self, seconds, minutes, hours) -> None:
        self.add_seconds(seconds)
        self.add_minutes(minutes)
        self.add_hours(hours)
        self.clock = Clock.convert_seconds_to_clock(
            Clock.convert_clock_to_seconds(self.hours, self.minutes, self.seconds))

    @property
    def clock(self) -> Clock:
        return self._clock

    @clock.setter
    def clock(self, val: Clock) -> None:
        check_type(val, Clock, class_name=self.__class__.__name__, property_name='clock')
        self._clock = val
        self._hours, self._minutes, self._seconds = self.clock.get_values()

    def add_seconds(self, val: ConvertibleToFloat):
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='seconds')
        self._seconds += val

    def add_hours(self, val: ConvertibleToFloat):
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='hours')
        self._hours += val

    def add_minutes(self, val: ConvertibleToFloat):
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='minutes')
        self._minutes += val

    @property
    def seconds(self) -> float:
        return self._seconds

    @seconds.setter
    def seconds(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='seconds')
        self._set_clock(seconds=val, minutes=self._minutes, hours=self._hours)

    @property
    def minutes(self) -> float:
        return self._minutes

    @minutes.setter
    def minutes(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='minutes')
        self._set_clock(self._seconds, val, self._hours)

    @property
    def hours(self) -> float:
        return self._hours

    @hours.setter
    def hours(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='hours')
        self._hours = float(val)
        self._set_clock(self._seconds, self._minutes, val)

    def calculate_in_seconds(self) -> float:
        return self._seconds + (60 * self._minutes) + (3600 * self._hours)

    def calculate_in_minutes(self) -> float:
        return (self._seconds / 60) + self._minutes + (60 * self._hours)

    def calculate_in_hours(self) -> float:
        return (self._seconds / 3600) + (self._minutes / 60) + self._hours

    def get_clock_as_string(self, mode: ClockMode = 'hms', round_: Optional[int] = None):
        return self.clock.get_as_string(mode, round_)

    def __abs__(self):
        return Duration(self.calculate_in_seconds().__abs__())

    def __add__(self, other):
        return Duration(self.calculate_in_seconds().__add__(other.calculate_in_seconds()))

    def __ceil__(self):
        return Duration(self.calculate_in_seconds().__ceil__())

    def __floor__(self):
        return Duration(self.calculate_in_seconds().__floor__())

    def __floordiv__(self, other):
        return Duration(self.calculate_in_seconds().__floordiv__(_convert_other(other)))

    def __gt__(self, other):
        return self.calculate_in_seconds().__gt__(_convert_other(other))

    def __ge__(self, other):
        return self.calculate_in_seconds().__ge__(_convert_other(other))

    def __hash__(self):
        return self.calculate_in_seconds().__hash__()

    def __le__(self, other):
        return self.calculate_in_seconds().__le__(_convert_other(other))

    def __lt__(self, other):
        return Duration(self.calculate_in_seconds().__lt__(_convert_other(other)))

    def __mod__(self, other):
        return Duration(self.calculate_in_seconds().__mod__(_convert_other(other)))

    def __mul__(self, other):
        return Duration(self.calculate_in_seconds().__mul__(_convert_other(other)))

    def __neg__(self):
        return self.calculate_in_seconds().__neg__()

    def __pos__(self):
        return self.calculate_in_seconds().__pos__()

    def __pow__(self, power, modulo=None):
        return Duration(self.calculate_in_seconds().__pos__(power, modulo))

    def __radd__(self, other):
        return Duration(self.calculate_in_seconds().__radd__(_convert_other(other)))

    def __rfloordiv__(self, other):
        return Duration(self.calculate_in_seconds().__rfloordiv__(_convert_other(other)))

    def __rmod__(self, other):
        return Duration(self.calculate_in_seconds().__rmod__(_convert_other(other)))

    def __rmul__(self, other):
        return Duration(self.calculate_in_seconds().__rmul__(_convert_other(other)))

    def __round__(self, n=None):
        return Duration(self.calculate_in_seconds().__round__(n))

    def __rpow__(self, other):
        return Duration(self.calculate_in_seconds().__rpow__(_convert_other(other)))

    def __rtruediv__(self, other):
        return Duration(self.calculate_in_seconds().__rtruediv__(_convert_other(other)))

    def __truediv__(self, other):
        return Duration(self.calculate_in_seconds().__truediv__(_convert_other(other)))

    def __trunc__(self):
        return self.calculate_in_seconds().__trunc__()

    def __eq__(self, other):
        return self.calculate_in_seconds().__eq__(_convert_other(other))


def convert_duration_to_quarter_duration(duration: Union[Duration, float, int],
                                         metronome: Union[Metronome, int]) -> QuarterDuration:
    if isinstance(duration, Duration):
        seconds = Fraction(duration.calculate_in_seconds())
    else:
        seconds = duration
    if isinstance(metronome, int):
        metronome = Metronome(metronome)

    quarter_per_minute = metronome.per_minute * metronome.beat_unit
    qd = Fraction(60 * seconds, quarter_per_minute)

    return QuarterDuration(qd)


def convert_quarter_duration_to_duration(quarter_duration: Union[QuarterDuration, float, int],
                                         metronome: Union[Metronome, int]) -> Duration:
    if not isinstance(quarter_duration, QuarterDuration):
        quarter_duration = QuarterDuration(quarter_duration)

    if isinstance(metronome, int):
        metronome = Metronome(metronome)

    quarter_per_minute = metronome.per_minute * metronome.beat_unit

    seconds = quarter_duration.value * 60 / quarter_per_minute
    return Duration(seconds=seconds)
