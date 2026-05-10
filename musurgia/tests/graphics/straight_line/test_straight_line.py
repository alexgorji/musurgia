from dataclasses import asdict
from pathlib import Path


from musurgia.graphics.defaults import DEFAULT_THICKNESS
from musurgia.graphics.geometry import Coordinates, LineOrientation, Position, Size
from musurgia.graphics.drawobject import LineOptions, StraightLine
from musurgia.graphics.svg.paginator import SVGPage
from musurgia.graphics.util import convert_to_scalar
from musurgia.tests.helpers.svg import SVGTestCase

path = Path(__file__)


def test_straight_line_get_bounding_box_coordinates():
    sl = StraightLine(type=LineOrientation.HORIZONTAL, length=10)
    assert sl.size == Size(10, DEFAULT_THICKNESS)
    assert sl.get_bounding_box_coordinates() == Coordinates(
        Position(0, -convert_to_scalar(DEFAULT_THICKNESS / 2)),
        Position(10, -convert_to_scalar(DEFAULT_THICKNESS / 2)),
        Position(10, convert_to_scalar(DEFAULT_THICKNESS / 2)),
        Position(0, convert_to_scalar(DEFAULT_THICKNESS / 2)),
    )


def test_straight_line_options():
    sl = StraightLine(
        type=LineOrientation.HORIZONTAL,
        length=10,
        options=LineOptions(color="red", stroke_dasharray=[5, 5]),
    )
    sl.options.thickness = 5

    assert asdict(sl.options) == {
        "color": "red",
        "thickness": 5,
        "stroke_dasharray": [5, 5],
    }


class LineDraw(SVGTestCase):
    def test_dashed_lines(self):
        page = SVGPage()
        hl = StraightLine(
            type=LineOrientation.HORIZONTAL,
            length=100,
            options=LineOptions(color="red", thickness=1, stroke_dasharray=[5, 5]),
        )
        page.add_draw_object(Position(10, 10), hl)
        page.add_background()
        page.add_grid()

        self.compare_page(page, "", path, width=297 * 2, height=210 * 2)
