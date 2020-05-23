from pathlib import Path

from musurgia.basic_functions import flatten
from musurgia.fractaltree.fractaltree import FractalTree
from musurgia.pdf.drawobject import DrawObject
from musurgia.pdf.line import HorizontalSegmentedLine
from musurgia.pdf.pdf import Pdf
from musurgia.unittest import TestCase

path = Path(__file__)


class DrawObjectRow(DrawObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._draw_objects = []

    def add_draw_object(self, draw_object):
        self._draw_objects.append(draw_object)

    @property
    def draw_objects(self):
        return self._draw_objects

    def get_relative_x2(self):
        return self.relative_x + sum([do.get_width() for do in self.draw_objects])

    def get_relative_y(self):
        return self.relative_y + max([do.get_height() for do in self.draw_objects])

    def draw(self, pdf):
        pdf.translate(self.relative_x, self.relative_y)
        pdf.add_object_margins(self)
        for do in self.draw_objects:
            do.draw(pdf)
            pdf.translate(0, do.get_width)


class DrawObjectColumn:
    pass


class GraphicalFractals(DrawObject):
    def __init__(self, fractal_tree, unit=1, distance=5, layer_range=None, large_marker_length=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer_range = layer_range
        self.large_marker_length = large_marker_length
        self._fractal_tree = None
        self._segmented_lines = []
        self._distance = distance
        self._unit = unit
        self.fractal_tree = fractal_tree

    def _make_segmented_lines(self):
        self._segmented_lines = []
        if self.layer_range is None:
            self.layer_range = [0, self.fractal_tree.number_of_layers + 1]
        distance = 0
        for layer_number in range(*self.layer_range):
            layer = self.fractal_tree.get_layer(layer_number)
            print(layer)
            lengths = [ch.value * self._unit for ch in layer]
            hsl = HorizontalSegmentedLine(lengths=lengths, relative_y=distance)
            self._segmented_lines.append(hsl)
            distance = self._distance

    @property
    def fractal_tree(self):
        return self._fractal_tree

    @fractal_tree.setter
    def fractal_tree(self, val):
        if not isinstance(val, FractalTree):
            raise TypeError(f"fractal_tree.value must be of type FractalTree not{type(val)}")
        self._fractal_tree = val
        self._make_segmented_lines()

    @property
    def segmented_lines(self):
        return self._segmented_lines

    def get_relative_x2(self):
        return self.relative_x + sum([hsl.get_height() for hsl in self.segmented_lines])

    def get_relative_y2(self):
        return self.relative_x + max([hsl.get_width() for hsl in self.segmented_lines])

    def draw(self, pdf):
        pdf.translate(self.relative_x, self.relative_y)
        with pdf.add_object_margins(self):
            for hsl in self.segmented_lines:
                hsl.draw(pdf)


class TestFractal(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_no_layer(self):
        ft = FractalTree(value=20)
        unit = 2
        gf = GraphicalFractals(fractal_tree=ft, unit=unit)
        gf.left_margin = 10
        gf.top_margin = 10

        with self.file_path(path, 'no_layer', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')

            gf.draw(self.pdf)

            self.pdf.write(pdf_path)

    def test_two_layer(self):
        ft = FractalTree(value=20)
        ft.add_layer()
        ft.add_layer()
        unit = 2
        gf = GraphicalFractals(fractal_tree=ft, unit=unit)
        gf.left_margin = 10
        gf.top_margin = 10

        with self.file_path(path, 'two_layer', 'pdf') as pdf_path:
            self.pdf.translate_page_margins()
            self.pdf.draw_ruler('h')
            self.pdf.draw_ruler('v')

            gf.draw(self.pdf)

            self.pdf.write(pdf_path)
