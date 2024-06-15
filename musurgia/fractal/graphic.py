import copy
from typing import cast

from musurgia.musurgia_exceptions import SegmentedLineSegmentHasMarginsError
from musurgia.pdf import DrawObjectRow, Pdf, DrawObjectColumn
from musurgia.pdf.line import LineSegment


class FractalTreeGraphic(DrawObjectColumn):
    def __init__(self, fractal_tree, distance=5, unit=1, mark_line_length: float = 6, shrink_factor=0.7, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._fractal_tree = fractal_tree
        self._unit = unit
        self._distance = distance
        self._mark_line_length = mark_line_length
        self._shrink_factor = shrink_factor
        self._create_graphic()

    def _create_graphic(self):
        for node in self.get_fractal_tree().traverse():
            if node == self.get_fractal_tree():
                chsl = ChildrenSegmentedLine(fractal_tree_children=[node], unit=self._unit,
                                             mark_line_length=self._mark_line_length,
                                             shrink_factor=self._shrink_factor)
                self.add_draw_object(chsl)
            if not node.is_leaf:
                markline_length = self._mark_line_length * (
                            self._shrink_factor * node.get_distance(self.get_fractal_tree()))
                chsl = ChildrenSegmentedLine(fractal_tree_children=node.get_children(), unit=self._unit,
                                             mark_line_length=markline_length,
                                             shrink_factor=self._shrink_factor)
                self.add_draw_object(chsl)
        # seg.unit = unit
        # self.chsl.add_draw_object(seg)

    def get_fractal_tree(self):
        return self._fractal_tree


class ChildrenSegmentedLine(DrawObjectRow):
    def __init__(self, fractal_tree_children, unit=1, mark_line_length=6, shrink_factor=0.7, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._children = fractal_tree_children
        self._unit = unit
        self._mark_line_length = mark_line_length
        self._shrink_factor = shrink_factor
        self._create_segments()

    def _create_segments(self):
        segments = [copy.deepcopy(node.get_node_segment()) for node in self.get_fractal_tree_children()]
        for seg in segments:
            seg.unit = self._unit
            seg.end_mark_line.length = self._mark_line_length
            seg.start_mark_line.length = self._mark_line_length
            if seg != segments[0]:
                seg.start_mark_line.length *= self._shrink_factor
            if seg != segments[-1]:
                seg.end_mark_line.length *= self._shrink_factor
            self.add_draw_object(seg)

    def _check_segment_margins(self):
        for seg in self.segments:
            if seg.margins != (0, 0, 0, 0):
                raise SegmentedLineSegmentHasMarginsError()

    @property
    def segments(self) -> list[LineSegment]:
        return cast(list[LineSegment], self.get_draw_objects())

    def get_fractal_tree_children(self):
        return self._children

    def set_straight_line_relative_y(self, val):
        delta = val - self.segments[0].straight_line.relative_y
        self.relative_y += delta

    def _align_segments(self):
        reference_segment = max(self.segments, key=lambda seg: seg.get_height())
        for segment in self.segments:
            if segment != reference_segment:
                segment.set_straight_line_relative_y(reference_segment.straight_line.relative_y)

    def draw(self, pdf: Pdf) -> None:
        self._check_segment_margins()
        self._align_segments()
        self.segments[-1].end_mark_line.show = True
        super().draw(pdf)
