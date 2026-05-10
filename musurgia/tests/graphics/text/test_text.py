from dataclasses import asdict
from pathlib import Path

import pytest

from musurgia.graphics.defaults import DEFAULT_COLOR
from musurgia.graphics.drawobject import Text, TextOptions
from musurgia.graphics.geometry import Paddings, Position
from musurgia.graphics.svg.paginator import SVGPage
from musurgia.tests.helpers.svg import SVGTestCase

path = Path(__file__)


def test_text_options():
    l1 = Text(text="test text", options=TextOptions(font_size=15))
    assert asdict(l1.options) == {
        "font_family": "DejaVu Sans",
        "font_size": 15,
        "color": DEFAULT_COLOR,
    }


def test_size():
    t = Text(text="Hello World")
    size = t.size
    assert size.width > 0
    assert size.height > 0
    size2 = t.size
    assert size == size2, f"Repeated measurement must be identical for {t.text}"


@pytest.mark.only
class TextDraw(SVGTestCase):
    def test_text_draw(self):
        l1 = Text(text="test text", options=TextOptions(font_size=15, color="red"))
        page = SVGPage()
        t1 = Text(
            text="The quick Brown fox Jumps over The lazy Dog",
        )

        t1.box.show = True
        page.add_draw_object(Position(30, 50), t1)

        t2 = Text(
            text="The quick Brown fox Jumps over The lazy Dog",
            padding=Paddings(20, 0, 0, 10),
            options=TextOptions(color="red"),
        )
        t2.box.show = True
        page.add_draw_object(Position(30, 100), t2)

        t3 = Text(
            text="The quick Brown fox Jumps over The lazy Dog",
            padding=Paddings(20, 30, 40, 10),
            options=TextOptions(color="orange", font_size=15),
        )
        t3.box.show = True

        page.add_draw_object(Position(30, 180), t3)
        page.add_background("white")
        page.add_grid()

        self.compare_page(
            page, "add_text_draw_object", path, width=210 * 2, height=297 * 2
        )
