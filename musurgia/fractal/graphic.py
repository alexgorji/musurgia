import copy
from typing import cast, Optional

from verysimpletree.tree import Tree, T

from musurgia.fractal import FractalTreeNodeSegment
from musurgia.musurgia_exceptions import SegmentedLineSegmentHasMarginsError
from musurgia.pdf import DrawObjectRow, Pdf, DrawObjectColumn
from musurgia.pdf.line import LineSegment


def _get_reference_segment(segments):
    end_mark_reference = max(segments, key=lambda seg: seg.end_mark_line.length)
    start_mark_reference = max(segments, key=lambda seg: seg.start_mark_line.length)
    reference_segment = start_mark_reference if start_mark_reference.start_mark_line.length >= end_mark_reference.end_mark_line.length else end_mark_reference
    return reference_segment


def get_largest_mark_line(segments):
    output = segments[0].start_mark_line
    for seg in segments:
        if seg.start_mark_line.length > output.length:
            output = seg.start_mark_line
        if seg.end_mark_line.length > output.length:
            output = seg.end_mark_line
    return output


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

        self._segment: FractalTreeNodeSegment
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
        self._graphic.add_draw_object(self.get_segment())
        if not self.is_leaf:
            second_row = DrawObjectRow()
            for ch in self.get_children():
                ch._create_graphic()
                second_row.add_draw_object(ch.get_graphic())
            self._graphic.add_draw_object(second_row)

    def _populate_tree(self):
        self._segment = FractalTreeNodeSegment(node_value=self.get_fractal_tree().get_value(), unit=self.unit)
        self._segment.start_mark_line.length = self.mark_line_length
        self._segment.end_mark_line.length = self.mark_line_length
        for ch in self.get_fractal_tree().get_children():
            self.add_child(GraphicTree(ch, unit=self.unit, mark_line_length=self.mark_line_length * self.shrink_factor))

    def _show_last_mark_lines(self):
        for node in self.traverse():
            if node.is_last_child:
                node.get_segment().end_mark_line.show = True

    def _update_mark_line_length(self):
        if self.is_first_child:
            self.get_segment().start_mark_line.length = self.mark_line_length
        else:
            self.get_segment().start_mark_line.length = round(self.mark_line_length * self.shrink_factor, 2)
        if self.is_last_child:
            self.get_segment().end_mark_line.length = self.mark_line_length

    def _update_mark_line_lengths(self):
        for node in self.traverse():
            node._update_mark_line_length()

    # def _align_layer_segments(self):
    #     for layer_number in range(1, self.get_number_of_layers() + 1):
    #         current_layer = self.get_layer(layer_number)
    #         segments = [l.get_segment() for l in current_layer]
    #         current_layer_largeste_mark_line = get_largest_mark_line(segments)
    #         for seg in segments:
    #             max_mark_line_length = max([seg.start_mark_line.length, seg.end_mark_line.length])
    #             dy = (current_layer_largeste_mark_line.length - max_mark_line_length) / 2
    #             seg.relative_y += dy
    def _update_distance(self):
        for node in self.traverse():
            if not node.is_leaf:
                node.get_graphic().get_draw_objects()[1].relative_y += node.distance

    def finalize(self):
        self._show_last_mark_lines()
        self._update_mark_line_lengths()
        self._update_distance()

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
            self._segment.unit = self.unit
        except AttributeError:
            pass

    @property
    def shrink_factor(self):
        return self._shrink_factor

    @shrink_factor.setter
    def shrink_factor(self, val):
        self._shrink_factor = val

    def get_segment(self):
        return self._segment

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
