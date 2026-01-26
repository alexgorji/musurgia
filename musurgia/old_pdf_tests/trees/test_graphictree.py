import copy
from pathlib import Path
from unittest import TestCase

from musurgia.trees.graphictree import (
    GraphicTree,
    ValuedTreeNodeSegment,
    GraphicChildrenSegmentedLine,
)
from musurgia.musurgia_exceptions import SegmentedLineSegmentHasMarginsError
from musurgia.pdf import DrawObjectColumn, DrawObjectRow, Pdf, draw_ruler, TextLabel
from musurgia.pdf.ruler import HorizontalRuler
from musurgia.tests.utils_for_tests import (
    PdfTestCase,
    create_test_valued_tree,
    add_node_infos_to_graphic,
)

path = Path(__file__)


class GraphicTreeTest(TestCase):
    def setUp(self):
        self.vt = create_test_valued_tree()
        # print(self.vt.get_tree_representation(key=lambda node: f"{node.get_position_in_tree()}: {node.get_duration().seconds}"))
        self.gt = GraphicTree(self.vt)

    def test_populate(self):
        traversed_ft = list(self.vt.traverse())
        traversed_gt = list(self.gt.traverse())
        assert len(traversed_ft) == len(traversed_gt)
        for fnode, gnode in zip(traversed_ft, traversed_gt):
            assert gnode.get_segment().length == float(fnode.get_value() * self.gt.unit)

    def test_set_node_value(self):
        seg = ValuedTreeNodeSegment(node_value=10)
        assert seg.length == 10
        assert seg.get_node_value() == 10
        seg.set_node_value(20)
        assert seg.get_node_value() == 20
        assert seg.length == 20
        seg.unit = 2
        assert seg.get_node_value() == 20
        assert seg.length == 40
        seg.set_node_value(10)
        assert seg.get_node_value() == 10
        assert seg.length == 20

    def test_node_segment(self):
        assert self.gt.get_segment().unit == 1
        segment = self.gt.get_segment()
        assert isinstance(segment, ValuedTreeNodeSegment)
        assert segment.length == self.vt.get_value()
        with self.assertRaises(AttributeError):
            segment.length = 10
        assert segment.start_mark_line.length == segment.end_mark_line.length == 6
        segment.unit = 10
        assert self.gt.get_segment().unit == 10
        assert segment.length == self.vt.get_value() * 10
        assert segment.start_mark_line.show
        assert not segment.end_mark_line.show
        segment.end_mark_line.show = True

        segment.start_mark_line.add_text_label("something")
        copied_segment = copy.deepcopy(segment)
        assert isinstance(copied_segment, ValuedTreeNodeSegment)
        assert copied_segment.unit == segment.unit
        assert copied_segment.length == self.vt.get_value() * 10
        assert copied_segment.start_mark_line.show
        assert segment.end_mark_line.show
        copied_segment.unit = 5
        assert segment.unit == 10
        copied_segment.end_mark_line.show = False
        assert segment.end_mark_line.show
        assert not copied_segment.end_mark_line.show
        assert copied_segment.start_mark_line.get_text_labels()[0].value == "something"

    def test_change_unit(self):
        self.gt.unit = 10
        for node in self.gt.traverse():
            assert node.unit == 10

    def test_graphic(self):
        for node in self.gt.traverse():
            assert isinstance(node.get_graphic(), DrawObjectColumn)
            if node.is_leaf:
                number_draw_objects = 1
            else:
                number_draw_objects = 2
            assert len(node.get_graphic().get_draw_objects()) == number_draw_objects
            assert node.get_graphic().get_draw_objects()[0] == node.get_segment()
            if not node.is_leaf:
                assert isinstance(
                    node.get_graphic().get_draw_objects()[1], DrawObjectRow
                )
                for ch, do in zip(
                    node.get_children(),
                    node.get_graphic().get_draw_objects()[1].get_draw_objects(),
                ):
                    assert isinstance(do, DrawObjectColumn)
                    assert do.get_draw_objects()[0] == ch.get_segment()

    def test_end_mark_lines(self):
        self.gt._show_last_mark_lines()
        for node in self.gt.traverse():
            if node.is_last_child:
                assert node.get_segment().end_mark_line.show is True
            else:
                assert node.get_segment().end_mark_line.show is False

    def test_mark_line_lengths(self):
        for node in self.gt.traverse():
            node._update_mark_line_length()
        for node in self.gt.traverse():
            if node.is_first_child:
                assert (
                    node.get_segment().start_mark_line.length == node.mark_line_length
                )
            else:
                self.assertAlmostEqual(
                    node.mark_line_length * node.shrink_factor,
                    node.get_segment().start_mark_line.length,
                )
            if node.is_last_child:
                assert node.get_segment().end_mark_line.length == node.mark_line_length

    def test_set_all_distances(self):
        self.gt.set_all_distances(20)
        for node in self.gt.traverse():
            assert node.distance == 20

    def test_wrong_child_type(self):
        with self.assertRaises(TypeError):
            self.gt.add_child("string")


class TestGraphicTreeDraw(PdfTestCase):
    def setUp(self):
        self.vt = create_test_valued_tree()
        self.gt = GraphicTree(self.vt)
        self.pdf = Pdf(orientation="l")
        add_node_infos_to_graphic(self.vt, self.gt)

    def test_draw_graphic(self):
        unit = 25
        self.gt.unit = unit
        self.gt.set_all_distances(20)

        with self.file_path(path, "draw", "pdf") as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, "h", unit=10, first_label=-1)
            draw_ruler(self.pdf, "v", unit=10)
            self.pdf.translate(10, 10)
            self.gt.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_draw_last_child_graphic(self):
        child = self.vt.get_children()[-1]
        child.update_value(15)
        graphic = GraphicTree(child, unit=10, distance=20)

        for index, (gn, fn) in enumerate(zip(graphic.traverse(), child.traverse())):
            text_label = TextLabel(f"{fn.get_position_in_tree()}", font_size=8)
            if gn.get_distance() > 1 and index % 2 == 1:
                text_label.placement = "below"
                text_label.top_margin = 1
            else:
                text_label.bottom_margin = 2
            gn.get_segment().start_mark_line.add_text_label(text_label)

        with self.file_path(path, "draw_last_child", "pdf") as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, "h", first_label=-1)
            draw_ruler(self.pdf, "v")
            self.pdf.translate(10, 10)
            graphic.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)

    def test_draw_clipped(self):
        unit = 15
        self.vt.update_value(50)
        gt = GraphicTree(self.vt, unit=unit, distance=5)
        add_node_infos_to_graphic(self.vt, gt)
        gt.set_all_distances(10)
        graphic = gt.get_graphic()
        graphic.bottom_margin = 15
        graphic._draw_objects = graphic._draw_objects[1:]
        c = DrawObjectColumn()
        c.bottom_margin = 10
        ruler = HorizontalRuler(unit=unit, length=graphic.get_width())
        c.add_draw_object(ruler)
        c.add_draw_object(graphic)

        with self.file_path(path, "draw_clipped", "pdf") as pdf_path:
            self.pdf.r_margin = self.pdf.l_margin = (self.pdf.w - 18 * unit) / 2
            self.pdf.translate_page_margins()
            c.clipped_draw(self.pdf)
            self.pdf.write_to_path(pdf_path)


class TestGraphicChildrenSegmentedLine(TestCase):
    def setUp(self):
        self.vt = create_test_valued_tree()
        self.gt = GraphicTree(self.vt)

    def test_check_segment_margins(self):
        gcsl = GraphicChildrenSegmentedLine(self.gt.get_children())
        gcsl.segments[0].margins = (1, 2, 3, 4)
        with self.assertRaises(SegmentedLineSegmentHasMarginsError):
            gcsl.draw(Pdf())

    def test_set_straight_line_relative_y(self):
        gcsl = GraphicChildrenSegmentedLine(self.gt.get_children())
        assert set([seg.get_height() for seg in gcsl.segments]) == {4.2}
        gcsl.set_straight_line_relative_y(0)
        assert set([seg.relative_y for seg in gcsl.segments]) == {0}
        assert gcsl.relative_y == -2.1


class TestCreatLayerGraphic(PdfTestCase):
    def setUp(self):
        self.vt = create_test_valued_tree()
        self.pdf = Pdf(orientation="l")

    def test_create_layer_graphic(self):
        unit = 24
        gt = GraphicTree(self.vt, unit=unit, distance=12, shrink_factor=0.6)
        add_node_infos_to_graphic(self.vt, gt)

        graphic = gt.get_graphic()
        graphic.bottom_margin = 30

        graphic_layer_2 = gt.create_layer_graphic(layer_number=2)
        graphic_layer_2.add_text_label(
            TextLabel(value="layer 2", placement="left", font_size=8, right_margin=2)
        )
        graphic_layer_2.bottom_margin = 20

        graphic_layer_3 = gt.create_layer_graphic(layer_number=3)
        graphic_layer_3.add_text_label(
            TextLabel(value="layer 3", placement="left", font_size=8, right_margin=2)
        )

        c = DrawObjectColumn()

        c.add_draw_object(graphic)
        c.add_draw_object(graphic_layer_2)
        c.add_draw_object(graphic_layer_3)

        with self.file_path(path, "draw_layers", "pdf") as pdf_path:
            self.pdf.translate_page_margins()
            draw_ruler(self.pdf, "h", unit=unit, first_label=-1)
            draw_ruler(self.pdf, "v", unit=unit)
            self.pdf.translate(unit, 10)
            c.draw(self.pdf)
            self.pdf.write_to_path(pdf_path)
