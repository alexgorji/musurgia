from typing import List
import svg
from musurgia.graphics.drawobject import (
    LineDrawObject,
    Position,
    TextDrawObject,
)


class ConvertTextDrawObjectToSVG:
    def __init__(self, position: Position, draw_object: TextDrawObject):
        self.position = position
        self.draw_object = draw_object

    def get_font_size_mm(self):
        return self.draw_object.font_size * 25.4 / 72

    def convert(self):
        return svg.Text(
            x=self.draw_object.start.x + self.position.x,
            y=self.draw_object.start.y + self.position.y,
            text=self.draw_object.text,
            font_size=self.get_font_size_mm(),
            font_family=self.draw_object.font_family,
            fill=self.draw_object.color,
        )


class ConvertLinDrawObjectToSVG:
    def __init__(self, position: Position, draw_object: LineDrawObject):
        self.position = position
        self.draw_object = draw_object

    def convert(self):
        return svg.Line(
            x1=self.draw_object.start.x + self.position.x,
            y1=self.draw_object.start.y + self.position.y,
            x2=self.draw_object.end.x + self.position.x,
            y2=self.draw_object.end.y + self.position.y,
            stroke=self.draw_object.color,
            stroke_width=self.draw_object.thickness,
        )
