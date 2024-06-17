import copy
from typing import cast

from verysimpletree.tree import Tree, T

from musurgia.musurgia_exceptions import SegmentedLineSegmentHasMarginsError
from musurgia.pdf import DrawObjectRow, Pdf, DrawObjectColumn, HorizontalLineSegment
from musurgia.pdf.line import LineSegment


class FractalTreeNodeSegment(HorizontalLineSegment):
    def __init__(self, node_value, unit=1, *args, **kwargs):
        super().__init__(length=node_value * unit, *args, **kwargs)
        self._node_value = node_value
        self._unit: int
        self.unit = unit

    def _update_length(self):
        self.straight_line.length = self.get_node_value() * self.unit

    @property
    def length(self) -> float:
        return super().length

    @property
    def unit(self) -> int:
        return self._unit

    @unit.setter
    def unit(self, value: int) -> None:
        self._unit = value
        self._update_length()

    def get_node_value(self):
        return self._node_value

    def set_node_value(self, val):
        self._node_value = val
        self._update_length()


class GraphicChildrenSegmentedLine(DrawObjectRow):
    def __init__(self, graphic_children, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._children = graphic_children
        self._create_segments()

    def _create_segments(self):
        segments = [copy.deepcopy(node.get_segment()) for node in self._children]
        for seg in segments:
            self.add_draw_object(seg)

    def _check_segment_margins(self):
        for seg in self.segments:
            if seg.margins != (0, 0, 0, 0):
                raise SegmentedLineSegmentHasMarginsError()

    @property
    def segments(self) -> list[LineSegment]:
        return cast(list[LineSegment], self.get_draw_objects())

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


class GraphicTree(Tree):
    def __init__(self, fractal_tree, distance=5, unit=1, mark_line_length=6, shrink_factor=0.7, *args,
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
        # self._create_graphic()

    def _check_child_to_be_added(self, child: T) -> bool:
        if not isinstance(child, GraphicTree):
            raise TypeError
        else:
            return True

    def _create_graphic(self):
        # output =  DrawObjectColumn()
        # output.add_draw_object(self.get_segment())
        # if not self.is_leaf:
        #     second_row = DrawObjectRow()
        #     for ch in self.get_children():
        #         ch._create_graphic()
        #         second_row.add_draw_object(ch.get_graphic())
        #     output.add_draw_object(second_row)
        # return output
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
            self.add_child(GraphicTree(ch, distance=self.distance, unit=self.unit,
                                       mark_line_length=self.mark_line_length * self.shrink_factor))

    def _show_last_mark_lines(self):
        for node in self.traverse():
            if node.is_last_child:
                node.get_segment().end_mark_line.show = True

    def _update_mark_line_length(self):
        if self.is_first_child:
            self.get_segment().start_mark_line.length = self.mark_line_length
        else:
            self.get_segment().start_mark_line.length = self.mark_line_length * self.shrink_factor
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
                node._graphic.get_draw_objects()[1].relative_y += node.distance

    def _finalize(self):
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
        self._mark_line_length = round(val, 5)

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = value
        for node in self.traverse():
            if node != self:
                node.unit = value
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

    def create_layer_graphic(self, layer_number):
        self._update_mark_line_lengths()
        children = self.get_layer(layer_number)
        return GraphicChildrenSegmentedLine(graphic_children=children)

    def get_segment(self):
        return self._segment

    def get_fractal_tree(self):
        return self._fractal_tree

    def get_graphic(self):
        for node in self.traverse():
            node._create_graphic()
        self._finalize()
        return self._graphic

    def set_all_distances(self, val):
        for node in self.traverse():
            node.distance = val

    def draw(self, pdf):
        self.get_graphic().draw(pdf)
