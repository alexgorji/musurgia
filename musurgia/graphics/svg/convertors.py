import svg
from musurgia.graphics.drawobject import LineDrawObject, TextDrawObject


class ConvertTextDrawObjectToSVG:
    def __init__(self, draw_object: TextDrawObject):
        self.draw_object = draw_object

    def get_absolute_x(self, state_position_x: int):
        return self.draw_object.layout.relative_x + state_position_x

    def get_absolute_y(self, state_position_y: int):
        return self.draw_object.layout.relative_y + state_position_y

    def get_font_size_mm(self):
        return self.draw_object.font_size * 25.4 / 72

    def convert(self):
        absolut_position = self.draw_object.layout.get_absolute_position()
        return svg.Text(
            x=absolut_position["x"],
            y=absolut_position["y"],
            text=self.draw_object.text,
            font_size=self.get_font_size_mm(),
            font_family=self.draw_object.font_family,
            fill=self.draw_object.color,
        )


class ConvertLinDrawObjectToSVG:
    def __init__(self, draw_object: LineDrawObject):
        self.draw_object = draw_object

    def convert(self):
        return svg.Line(
            x1=self.draw_object.start["x"],
            y1=self.draw_object.start["y"],
            x2=self.draw_object.end["x"],
            y2=self.draw_object.end["y"],
            stroke="blue",
            stroke_width=2,
        )
