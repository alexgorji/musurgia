from abc import ABC
from typing import Any

from musurgia.musurgia_types import create_error_message
from musurgia.pdf.labeled import Labeled
from musurgia.pdf.drawobject import DrawObject
from musurgia.pdf.margined import Margined
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.positioned import Positioned


class DrawObjectContainer(DrawObject, Labeled, Positioned, Margined, ABC):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._draw_objects = []

    def add_draw_object(self, draw_object: DrawObject) -> DrawObject:
        if not isinstance(draw_object, DrawObject):
            raise TypeError(create_error_message(class_name=self.__class__.__name__, method_name='add_draw_object',
                                                 argument_name='draw_object',
                                                 message=f'draw_object must be of type DrawObject, not {type(draw_object)}'))
        self._draw_objects.append(draw_object)
        return draw_object

    @property
    def draw_objects(self) -> list[DrawObject]:
        return self._draw_objects


class DrawObjectRow(DrawObjectContainer):

    def get_relative_x2(self) -> float:
        return self.relative_x + sum([do.get_width() for do in self.draw_objects])

    def get_relative_y2(self) -> float:
        return self.relative_y + max([do.get_height() for do in self.draw_objects])

    def draw(self, pdf: Pdf) -> None:
        with pdf.prepare_draw_object(self):
            self.draw_above_text_labels(pdf)
            self.draw_left_text_labels(pdf)
            if self.get_below_text_labels():
                self.draw_below_text_labels(pdf)
            for do in self.draw_objects:
                do.draw(pdf)
                pdf.translate(do.get_width(), 0)


class DrawObjectColumn(DrawObjectContainer):
    def get_relative_x2(self) -> float:
        return self.relative_x + max([do.get_width() for do in self.draw_objects])

    def get_relative_y2(self) -> float:
        return self.relative_y + sum([do.get_height() for do in self.draw_objects])

    def draw(self, pdf: Pdf) -> None:
        with pdf.prepare_draw_object(self):
            self.draw_above_text_labels(pdf)
            self.draw_left_text_labels(pdf)
            if self.get_below_text_labels():
                self.draw_below_text_labels(pdf)
            for do in self.draw_objects:
                do.draw(pdf)
                pdf.translate(0, do.get_height())
