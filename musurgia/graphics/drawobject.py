from dataclasses import dataclass


@dataclass
class DrawObjectLayout:
    relative_x: int
    relative_y: int


@dataclass
class DrawObject:
    layout: DrawObjectLayout


@dataclass
class TextDrawObject(DrawObject):
    text: str
