import copy
from typing import cast, Optional

from verysimpletree.tree import Tree, T

from musurgia.fractal import FractalTreeNodeSegment
from musurgia.musurgia_exceptions import SegmentedLineSegmentHasMarginsError
from musurgia.pdf import DrawObjectRow, Pdf, DrawObjectColumn
from musurgia.pdf.line import LineSegment


class GraphicTree(Tree):
    def __init__(self, fractal_tree, distance=5, unit=10, mark_line_length=6, shrink_factor=0.7, *args,
                 **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._fractal_tree = fractal_tree
        self._distance: int
        self._unit: int
        self._mark_line_length: float
        self._shrink_factor: float

        self.distance = distance
        self.unit = unit
        self.mark_line_length = mark_line_length
        self.shrink_factor = shrink_factor

        self._node_segment: FractalTreeNodeSegment
        self._graphic: DrawObjectColumn
        self._populate_tree()
        self._create_graphic()

    def _check_child_to_be_added(self, child: T) -> bool:
        if not isinstance(child, GraphicTree):
            raise TypeError
        else:
            return True

    def _create_graphic(self):
        self._graphic = DrawObjectColumn()
        self._graphic.add_draw_object(self.get_node_segment())
        if not self.is_leaf:
            second_row = DrawObjectRow()
            for ch in self.get_children():
                ch._create_graphic()
                second_row.add_draw_object(ch.get_graphic())
            self._graphic.add_draw_object(second_row)

    def _populate_tree(self):
        self._node_segment = FractalTreeNodeSegment(node_value=self.get_fractal_tree().get_value(), unit=self.unit)
        for ch in self.get_fractal_tree().get_children():
            self.add_child(GraphicTree(ch))

    def _show_last_mark_lines(self):
        for node in self.traverse():
            if node.is_last_child:
                node.get_node_segment().end_mark_line.show = True

    def finalize(self):
        self._show_last_mark_lines()

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, val):
        self._distance = val

    @property
    def mark_line_length(self):
        return self._mark_line_length

    @mark_line_length.setter
    def mark_line_length(self, val):
        self._mark_line_length = val

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = value
        try:
            self._node_segment.unit = self.unit
        except AttributeError:
            pass

    @property
    def shrink_factor(self):
        return self._shrink_factor

    @shrink_factor.setter
    def shrink_factor(self, val):
        self._shrink_factor = val

    def get_node_segment(self):
        return self._node_segment

    def get_fractal_tree(self):
        return self._fractal_tree

    def get_graphic(self):
        return self._graphic

    def draw(self, pdf):
        self.finalize()
        self.get_graphic().draw(pdf)

        # gr = DrawObjectColumn()
        # first_row = gr.add_draw_object(DrawObjectRow())
        # segment = copy.deepcopy(self.get_node_segment())
        # segment.unit = unit
        # if layer_number == 1:
        #     segment.end_mark_line.length = segment.start_mark_line.length = mark_line_length
        #     segment.end_mark_line.show = True
        #     children_layer_top_margin = 0
        # else:
        #     segment.end_mark_line.length = segment.start_mark_line.length = mark_line_length * shrink_factor
        #     children_layer_top_margin = (mark_line_length - segment.start_mark_line.length)
        #     # children_layer_top_margin = 0
        #     if self.is_last_child:
        #         segment.end_mark_line.length = mark_line_length
        #         segment.end_mark_line.show = True
        #         children_layer_top_margin = 0
        #     if self.is_first_child:
        #         segment.start_mark_line.length = mark_line_length
        #         children_layer_top_margin = 0
        # segment.bottom_margin += distance
        # segment.top_margin += layer_top_margin
        # first_row.add_draw_object(segment)
        # if not self.is_leaf:
        #     second_row = gr.add_draw_object(DrawObjectRow())
        #     for ch in self.get_children():
        #         second_row.add_draw_object(
        #             ch.create_graphic(distance, unit, mark_line_length * shrink_factor, shrink_factor,
        #                               layer_number + 1, children_layer_top_margin))
        #
        # return gr

        # class FractalTreeGraphic(DrawObjectColumn):
        #     def __init__(self, fractal_tree, distance=5, unit=1, mark_line_length: float = 6, shrink_factor=0.7, *args,
        #                  **kwargs):
        #         super().__init__(*args, **kwargs)
        #         self._fractal_tree = fractal_tree
        #         self._unit = unit
        #         self._distance = distance
        #         self._mark_line_length = mark_line_length
        #         self._shrink_factor = shrink_factor
        #         self._create_graphic()
        #
        #     def _create_graphic(self):
        #         for node in self.get_fractal_tree().traverse():
        #             if node == self.get_fractal_tree():
        #                 chsl = ChildrenSegmentedLine(fractal_tree_children=[node], unit=self._unit,
        #                                              mark_line_length=self._mark_line_length,
        #                                              shrink_factor=self._shrink_factor)
        #                 self.add_draw_object(chsl)
        #             if not node.is_leaf:
        #                 markline_length = self._mark_line_length * (
        #                             self._shrink_factor * node.get_distance(self.get_fractal_tree()))
        #                 chsl = ChildrenSegmentedLine(fractal_tree_children=node.get_children(), unit=self._unit,
        #                                              mark_line_length=markline_length,
        #                                              shrink_factor=self._shrink_factor)
        #                 self.add_draw_object(chsl)
        #         # seg.unit = unit
        #         # self.chsl.add_draw_object(seg)
        #
        #     def get_fractal_tree(self):
        #         return self._fractal_tree
        #
        #
        # class ChildrenSegmentedLine(DrawObjectRow):
        #     def __init__(self, fractal_tree_children, unit=1, mark_line_length=6, shrink_factor=0.7, *args, **kwargs):
        #         super().__init__(*args, **kwargs)
        #         self._children = fractal_tree_children
        #         self._unit = unit
        #         self._mark_line_length = mark_line_length
        #         self._shrink_factor = shrink_factor
        #         self._create_segments()
        #
        #     def _create_segments(self):
        #         segments = [copy.deepcopy(node.get_node_segment()) for node in self.get_fractal_tree_children()]
        #         for seg in segments:
        #             seg.unit = self._unit
        #             seg.end_mark_line.length = self._mark_line_length
        #             seg.start_mark_line.length = self._mark_line_length
        #             if seg != segments[0]:
        #                 seg.start_mark_line.length *= self._shrink_factor
        #             if seg != segments[-1]:
        #                 seg.end_mark_line.length *= self._shrink_factor
        #             self.add_draw_object(seg)
        #
        #     def _check_segment_margins(self):
        #         for seg in self.segments:
        #             if seg.margins != (0, 0, 0, 0):
        #                 raise SegmentedLineSegmentHasMarginsError()
        #
        #     @property
        #     def segments(self) -> list[LineSegment]:
        #         return cast(list[LineSegment], self.get_draw_objects())
        #
        #     def get_fractal_tree_children(self):
        #         return self._children
        #
        #     def set_straight_line_relative_y(self, val):
        #         delta = val - self.segments[0].straight_line.relative_y
        #         self.relative_y += delta
        #
        #     def _align_segments(self):
        #         reference_segment = max(self.segments, key=lambda seg: seg.get_height())
        #         for segment in self.segments:
        #             if segment != reference_segment:
        #                 segment.set_straight_line_relative_y(reference_segment.straight_line.relative_y)
        #
        #     def draw(self, pdf: Pdf) -> None:
        #         self._check_segment_margins()
        #         self._align_segments()
        #         self.segments[-1].end_mark_line.show = True
        #         super().draw(pdf)
