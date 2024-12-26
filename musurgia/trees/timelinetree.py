from fractions import Fraction
from typing import Any, Union

from musicscore.metronome import Metronome
from musicscore.quarterduration import QuarterDuration

from musurgia.chordfactory.chordfactory import AbstractChordFactory
from musurgia.timing.duration import (
    ReadonlyDuration,
    convert_duration_to_quarter_duration_value,
)
from musurgia.trees.valuedtree import ValuedTree
from musurgia.musurgia_types import ConvertibleToFraction, MusurgiaTypeError, check_type

__all__ = ["TimelineDuration", "TimelineTree"]


class TimelineDuration(ReadonlyDuration):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._metronome: "Metronome" = Metronome(60)
        self._quarter_duration: "QuarterDuration" = QuarterDuration(1)

    def _set_seconds(self, seconds: ConvertibleToFraction) -> None:
        self._set_clock(hours=0, minutes=0, seconds=seconds)

    @property
    def metronome(self) -> "Metronome":
        return self._metronome

    @metronome.setter
    def metronome(self, value: "Metronome") -> None:
        if not isinstance(value, Metronome):
            raise TypeError
        self._metronome = value

    @property
    def quarter_duration(self) -> None:
        raise AttributeError("Use get_duration() instead.")

    @quarter_duration.setter
    def quarter_duration(self, value: Any) -> None:
        raise AttributeError("TimelineDuration.quarter_duration cannot be set.")

    def get_quarter_duration(self) -> QuarterDuration:
        self._quarter_duration.value = convert_duration_to_quarter_duration_value(
            self.metronome, self.calculate_in_seconds()
        )
        return self._quarter_duration

    def get_metronome(self) -> Metronome:
        return self._metronome


class TimelineTree(ValuedTree):
    def __init__(
        self,
        duration: Union[TimelineDuration, ConvertibleToFraction],
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        if not isinstance(duration, TimelineDuration):
            try:
                check_type(duration, "ConvertibleToFraction")
            except MusurgiaTypeError:
                raise AttributeError(
                    "TimelineTree.update_duration: duration must be of of types TimelineDuration or ConvertibleToFraction"
                )
            duration = TimelineDuration(duration)
        self._duration: TimelineDuration = duration

    # private methods
    def _check_child_to_be_added(self, child: "TimelineTree") -> bool:
        if not isinstance(child, TimelineTree):
            raise TypeError(
                f"Wrong child type. Child must be of type FractalTree not {type(child)}"
            )
        return True

    def _set_value(self, value: ConvertibleToFraction) -> None:
        if not isinstance(value, Fraction):
            value = Fraction(value)
        self._duration._set_seconds(value)

    @property
    def duration(self) -> None:
        raise AttributeError("Use get_duration() instead.")

    def get_duration(self) -> TimelineDuration:
        return self._duration

    def get_value(self) -> Fraction:
        return self.get_duration().calculate_in_seconds()

    def update_duration(
        self, duration: Union[TimelineDuration, ConvertibleToFraction]
    ) -> None:
        if isinstance(duration, TimelineDuration):
            self._duration = duration
            new_value = self.get_value()
        elif isinstance(duration, Fraction):
            new_value = duration
        else:
            try:
                check_type(duration, "ConvertibleToFraction")
            except MusurgiaTypeError:
                raise AttributeError(
                    "TimelineTree.update_duration: duration must be of of types TimelineDuration or ConvertibleToFraction"
                )
            new_value = Fraction(duration)
        self.update_value(new_value)


class SimpleTimelineChordFactory(AbstractChordFactory):
    def __init__(
        self,
        timline_node: TimelineTree,
        show_metronome: bool = False,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self._timeline_node: TimelineTree = timline_node
        self._show_metronome: bool
        self.show_metronome = show_metronome

    @property
    def show_metronome(self) -> bool:
        return self._show_metronome

    @show_metronome.setter
    def show_metronome(self, value: bool) -> None:
        self._show_metronome = value

    def update_chord_midis(self) -> None:
        self._chord.midis = 72

    def update_chord_quarter_duration(self) -> None:
        self._chord.quarter_duration = (
            self._timeline_node.get_duration().get_quarter_duration()
        )

    def update_chord_metronome(self) -> None:
        if self.show_metronome:
            self._chord.metronome = self._timeline_node.get_duration().get_metronome()
