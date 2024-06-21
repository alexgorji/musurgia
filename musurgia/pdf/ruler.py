from abc import ABC
from typing import Any

from musurgia.musurgia_types import ConvertibleToFloat, check_type
from musurgia.pdf import TextLabel, Pdf
from musurgia.pdf.line import AbstractSegmentedLine, MarkLine, VerticalSegmentedLine, HorizontalSegmentedLine


class AbstractRuler(AbstractSegmentedLine, ABC):
    def __init__(self, length: ConvertibleToFloat, unit: ConvertibleToFloat = 10.0, first_label: int = 0,
                 label_show_interval: int = 1, show_first_label: bool = True, *args: Any, **kwargs: Any):
        check_type(length, 'ConvertibleToFloat', class_name='AbstractRuler', property_name='length')
        check_type(unit, 'ConvertibleToFloat', class_name='AbstractRuler', property_name='unit')
        check_type(first_label, int, class_name='AbstractRuler', property_name='first_label')
        check_type(label_show_interval, int, class_name='AbstractRuler', property_name='label_show_interval')
        check_type(show_first_label, int, class_name='AbstractRuler', property_name='show_first_label')

        unit = float(unit)
        number_of_units = float(length) / unit
        partial_segment_length = number_of_units - int(number_of_units)
        lengths = int(number_of_units) * [unit]
        if partial_segment_length:
            lengths += [partial_segment_length * unit]
        super().__init__(lengths=lengths, *args, **kwargs)  # type: ignore
        if partial_segment_length:
            self.segments[-1].end_mark_line.show = False

        self.unit = unit
        self.first_label = first_label
        self.label_show_interval = label_show_interval
        self.show_first_label = show_first_label
        self._set_labels()

    @property
    def length(self) -> float:
        return sum([s.length for s in self.segments])

    def _set_labels(self) -> None:
        def _add_label(mark_line: MarkLine, txt: str) -> None:
            tl = TextLabel(txt, master=mark_line)
            if isinstance(self, VerticalSegmentedLine):
                tl.placement = 'left'
                tl.right_margin = 1
                tl.top_margin = 0
            else:
                tl.bottom_margin = 1
            mark_line.add_text_label(tl)

        for index, segment in enumerate(self.segments):
            if not self.show_first_label and index == 0:
                pass
            else:
                if index % self.label_show_interval == 0:
                    mark_line = segment.start_mark_line
                    _add_label(mark_line, str(index + self.first_label))

        last_segment_end_mark_line = self.segments[-1].end_mark_line
        if last_segment_end_mark_line.show and (len(self.segments)) % self.label_show_interval == 0:
            _add_label(last_segment_end_mark_line, str(len(self.segments) + self.first_label))


class HorizontalRuler(AbstractRuler, HorizontalSegmentedLine):
    pass


class VerticalRuler(AbstractRuler, VerticalSegmentedLine):
    pass


class TimeRuler(HorizontalRuler):
    pass
