from musurgia.graphics.drawobject import DrawObject, Position
from musurgia.graphics.svg.convertors import SVGConverterRegistry


import svg


from typing import Literal


def create_svg_object(
    width: int | float,
    height: int | float,
    positioned_draw_objects: list[tuple[Position, DrawObject]],
    unit: Literal["em", "ex", "px", "pt", "pc", "cm", "mm", "in", "%"] = "mm",
) -> svg.SVG:
    svg_object = svg.SVG(
        width=svg.Length(width, unit),
        height=svg.Length(height, unit),
        viewBox=svg.ViewBoxSpec(0, 0, width, height),
    )

    if positioned_draw_objects:
        if svg_object.elements is None:
            svg_object.elements = []
        for position, draw_object in positioned_draw_objects:
            svg_object.elements.extend(
                SVGConverterRegistry.convert(position, draw_object)
            )
    return svg_object
