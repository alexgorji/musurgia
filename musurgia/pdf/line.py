from quicktions import Fraction

from musurgia.pdf.masterslave import Master, Slave
from musurgia.pdf.named import Named
from musurgia.pdf.newdrawobject import DrawObject


class StraightLine(Slave, DrawObject):
    def __init__(self, mode, length, show=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mode = None
        self._length = None

        self.mode = mode
        self.length = length
        self.show = show

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, val):
        permitted = ['h', 'horizontal', 'v', 'vertical']
        if val not in permitted:
            raise ValueError(f'mode.value {val} must be in {permitted}')
        self._mode = val

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, val):
        if not isinstance(val, float) and not isinstance(val, int) and not isinstance(val, Fraction):
            raise TypeError(f"length.value must be of type float, int or Fraction  not{type(val)}")
        self._length = val

    @staticmethod
    def get_opposite_mode(mode):
        if mode == 'h':
            return 'v'
        elif mode == 'v':
            return 'h'
        elif mode == 'horizontal':
            return 'vertical'
        elif mode == 'vertical':
            return 'horizontal'
        else:
            raise AttributeError()

    def get_relative_x2(self):
        if self.mode in ['h', 'horizontal']:
            return self.relative_x + self.length
        else:
            return self.relative_x

    def get_relative_y2(self):
        if self.mode in ['v', 'vertical']:
            return self.relative_y + self.length
        else:
            return self.relative_y

    def draw(self, pdf):
        if self.show:
            pdf.translate(self.relative_x, self.relative_y)
            x2 = self.get_relative_x2() - self.relative_x
            y2 = -(self.get_relative_y2() - self.relative_y)
            with pdf.add_margins(self):
                pdf.line(0, 0, x2, y2)


class MarkLine(StraightLine, DrawObject):
    def __init__(self, placement, length=3, y_offset=0, *args, **kwargs):
        super().__init__(length=length, *args, **kwargs)
        self._placement = None
        self._y_offset = None

        self.placement = placement
        self._y_offset = y_offset

    @property
    def placement(self):
        return self._placement

    @placement.setter
    def placement(self, val):
        permitted = ['start', 'end']
        if val not in permitted:
            raise ValueError(f'placement.value {val} must be in {permitted}')
        self._placement = val

    @property
    def y_offset(self):
        return self._y_offset

    @y_offset.setter
    def y_offset(self, val):
        self._y_offset = val


class LineSegment(Master, DrawObject):
    def __init__(self, mode, length, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._straight_line = StraightLine(name='straight_line', mode=mode, length=length, master=self)
        marker_mode = StraightLine.get_opposite_mode(self.mode)
        self._start_mark_line = MarkLine(name='start_mark_line', mode=marker_mode, master=self, placement='start')
        self._end_mark_line = MarkLine(name='end_mark_line', mode=marker_mode, master=self, placement='end', show=False)

    @property
    def straight_line(self):
        return self._straight_line

    @property
    def start_mark_line(self):
        return self._start_mark_line

    @property
    def end_mark_line(self):
        return self._end_mark_line

    @property
    def mode(self):
        return self.straight_line.mode

    @property
    def length(self):
        return self.straight_line.length

    def draw(self, pdf):
        with pdf.add_margins(self):
            self.straight_line.draw(pdf)
            self.start_mark_line.draw(pdf)
            self.end_mark_line.draw(pdf)


class HorizontalLineSegment(LineSegment):
    def __init__(self, length, *args, **kwargs):
        super().__init__(mode='horizontal', length=length, *args, **kwargs)

    def get_relative_x2(self):
        return self.left_margin + self.length + self.right_margin

    def get_relative_y2(self):
        return self.top_margin + self.straight_line.top_margin + self.straight_line.bottom_margin + self.bottom_margin

    def _get_straight_line_margin(self, margin):
        if margin in ['l', 'left']:
            return 0
        elif margin in ['r', 'right']:
            return 0
        elif margin in ['t', 'top']:
            return max([ml.length / 2 + ml.y_offset for ml in [self.start_mark_line, self.end_mark_line]])
        elif margin in ['b', 'bottom']:
            return max([ml.length / 2 - ml.y_offset for ml in [self.start_mark_line, self.end_mark_line]])
        else:
            raise AttributeError(margin)

    def _get_mark_line_margin(self, margin, mark_line):
        if margin in ['l', 'left']:
            return 0
        elif margin in ['r', 'right']:
            return 0
        elif margin in ['t', 'top']:
            return self._get_straight_line_margin('top') - (mark_line.length / 2 + mark_line.y_offset)
        elif margin in ['b', 'bottom']:
            return self._get_straight_line_margin('bottom') - (mark_line.length / 2 - mark_line.y_offset)
        else:
            raise AttributeError(margin)

    def _get_straight_line_position(self, position):
        if position == 'x':
            return 0
        elif position == 'y':
            return 0
        else:
            raise AttributeError(position)

    def _get_mark_line_position(self, position, mark_line):
        if position == 'x':
            if mark_line.placement == 'start':
                return 0
            else:
                return self.length
        elif position == 'y':
            return 0
        else:
            raise AttributeError(position)

    def get_slave_margin(self, slave, margin):
        if self.mode in ['h', 'horizontal']:
            if slave.name == 'straight_line':
                return self._get_straight_line_margin(margin)
            elif slave.name == 'start_mark_line':
                return self._get_mark_line_margin(margin, slave)
            elif slave.name == 'end_mark_line':
                return self._get_mark_line_margin(margin, slave)
            else:
                raise AttributeError(slave)
        else:
            raise NotImplementedError()

    def get_slave_position(self, slave, position):
        if self.mode in ['h', 'horizontal']:
            if slave.name == 'straight_line':
                return self._get_straight_line_position(position)
            elif slave.name == 'start_mark_line':
                return self._get_mark_line_position(position, slave)
            elif slave.name == 'end_mark_line':
                return self._get_mark_line_position(position, slave)
            else:
                raise AttributeError(slave)
        else:
            NotImplementedError()


class HorizontalSegmentedLine(DrawObject):
    def __init__(self, lengths, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._segments = None
        self._make_segments(lengths)

    @property
    def lengths(self):
        return [segment.length for segment in self.segments]

    @property
    def segments(self):
        return self._segments

    def _make_segments(self, lengths):
        if not lengths:
            raise AttributeError('lengths must be set.')
        self._segments = [HorizontalLineSegment(length) for length in lengths]
        self._segments[-1].end_mark_line.show = True

    def get_relative_x2(self):
        return self.relative_x + sum(self.lengths)

    def get_relative_y2(self):
        return self.relative_y + max([segment.get_height() for segment in self.segments])

    def draw(self, pdf):
        with pdf.add_margins(self):
            for segment in self.segments:
                segment.draw(pdf)
                pdf.translate(segment.get_width(), -segment.get_height())

# class HorizontalLine(DrawObject, Labeled, Named):
#     def __init__(self, length, factor=1, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._length = None
#         self._factor = None
#         self.length = length
#         self.factor = factor
#         self._start_mark_line = MarkLine(parent=self, placement='start')
#         self._end_mark_line = MarkLine(parent=self, placement='end', show=False)
#
#     @property
#     def factor(self):
#         if self._factor is None:
#             self._factor = 1
#         return self._factor
#
#     @factor.setter
#     def factor(self, val):
#         self._factor = val
#
#     @property
#     def length(self):
#         return self._length
#
#     @length.setter
#     def length(self, val):
#         self._length = val
#
#     @property
#     def actual_length(self):
#         return self.length * self.factor
#
#     @property
#     def start_mark_line(self):
#         return self._start_mark_line
#
#     @property
#     def end_mark_line(self):
#         return self._end_mark_line
#
#     def get_relative_x2(self):
#         return self.relative_x + self.actual_length + self.left_margin + self.right_margin
#
#     def get_relative_y2(self):
#         return max([ml.get_height() + self.top_margin + self.bottom_margin for ml in
#                     [self.start_mark_line, self.end_mark_line]])
#
#     @DrawObject.relative_y.getter
#     def relative_y(self):
#         if self.parent:
#             return self.parent.relative_y
#         else:
#             return self._relative_y
#
#     @DrawObject.relative_y.setter
#     def relative_y(self, val):
#         if self.parent:
#             raise RelativeYNotSettableError()
#         self._relative_y = val
#
#     def draw(self, pdf, translate=True):
#         if translate:
#             pdf.translate(self.relative_x, -self.relative_y)
#             x1 = 0
#             y = 0
#         else:
#             x1 = self.relative_x
#             y = self.relative_y
#
#         pdf.translate(self.left_margin, -self.top_margin)
#         x2 = self.actual_length
#
#         if self.name:
#             self.name.draw(pdf)
#
#         if self.show:
#             self.start_mark_line.draw(pdf)
#             self.end_mark_line.draw(pdf)
#             pdf.line(x1=x1, y1=y, x2=x2, y2=y)
#             for text_label in self._text_labels:
#                 text_label.draw(pdf)
#         pdf.translate(self.right_margin, -self.bottom_margin)
#
#
# class SegmentedHorizontalLine(DrawObject, Labeled, Named):
#     def __init__(self, lengths, factor=1, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._segments = []
#         self._factor = None
#         self.factor = factor
#         self._set_lengths(lengths)
#
#     def _add_length(self, length):
#         segment = HorizontalLine(length=length)
#         segment.parent = self
#         self._segments.append(segment)
#
#     def _set_lengths(self, lengths):
#         for length in lengths:
#             self._add_length(length)
#
#     @property
#     def actual_lengths(self):
#         return [segment.acutal_length for segment in self.segments]
#
#     @property
#     def factor(self):
#         return self._factor
#
#     @factor.setter
#     def factor(self, val):
#         for segment in self.segments:
#             segment.factor = val
#         self._factor = val
#
#     @property
#     def actual_length(self):
#         return sum([segment.acutal_length for segment in self.segments])
#
#     @property
#     def segments(self):
#         return self._segments
#
#     def get_relative_x2(self):
#         return self.relative_x + self.actual_length
#
#     def get_relative_y2(self):
#         return max([segment.get_relative_y2() for segment in self.segments])
#
#     def draw(self, pdf):
#         pdf.translate(self.relative_x, self.relative_y)
#         pdf.translate(self.left_margin, -self.top_margin)
#         for segment in self.segments:
#             segment.draw(pdf)
#             pdf.translate(segment.actual_length, 0)
#         pdf.translate(self.right_margin, self.bottom_margin)
