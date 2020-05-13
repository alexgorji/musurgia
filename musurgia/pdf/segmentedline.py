from musurgia.pdf.drawobject import DrawObject
from musurgia.pdf.labeled import Labeled
from musurgia.pdf.linesegment import LineSegment
from musurgia.pdf.named import Named


class SegmentedLine(DrawObject, Labeled, Named):
    def __init__(self, lengths, factor=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._line_segments = []
        self._factor = None
        self.factor = factor
        self._lengths = None
        self.lengths = lengths

    @DrawObject.relative_y.setter
    def relative_y(self, val):
        self._relative_y = val
        try:
            for line in self.line_segments:
                line.relative_y = val
        except AttributeError:
            pass

    @DrawObject.relative_x.setter
    def relative_x(self, val):
        self._relative_x = val
        try:
            self.line_segments[-1].relative_x = val
        except AttributeError:
            pass

    @property
    def lengths(self):
        return self._lengths

    @lengths.setter
    def lengths(self, val):
        if not isinstance(val, list):
            raise TypeError('lengths.value must be of type list not{}'.format(type(val)))
        self._lengths = val
        self._generate_line_segments()

    @property
    def line_segments(self):
        return self._line_segments

    def _generate_line_segments(self):
        self._line_segments = []
        for length in self.lengths:
            line_segement = LineSegment(length=length, relative_y=self.relative_y, factor=self.factor)
            if not self._line_segments:
                line_segement.relative_x = self.relative_x
            else:
                line_segement.relative_x = 0

            self._line_segments.append(line_segement)
        self._line_segments[-1].end_mark_line.show = True

    def get_relative_x2(self):
        raise Exception('SegementedLine does not have a x2 value')

    def get_relative_y2(self):
        return self.line_segments[0].relative_y

    def draw(self, pdf):
        for text_label in self._text_labels:
            text_label.draw(pdf)

        for line_segment in self.line_segments:
            if line_segment == self.line_segments[0]:
                line_segment.name = self.name

            line_segment.draw_with_break(pdf)
            new_x = pdf.x

            if line_segment._line_break and self.name:
                line_segment.name = self.name
                pdf.x = new_x - line_segment.actual_length
                line_segment.name.draw(pdf)
                pdf.x = new_x
