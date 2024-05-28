from abc import ABC, abstractmethod
from math import ceil
from typing import Optional, Union

from musurgia.musurgia_exceptions import PdfAttributeError
from musurgia.musurgia_types import create_error_message, check_type, ConvertibleToFloat
from musurgia.pdf.pdf import Pdf


class Margined:
    """
    An interface for setting and getting DrawObject's margin attributes.
    """

    def __init__(self, top_margin: ConvertibleToFloat = 0,
                 bottom_margin: ConvertibleToFloat = 0, left_margin: ConvertibleToFloat = 0,
                 right_margin: ConvertibleToFloat = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._top_margin: float = 0
        self._left_margin: float = 0
        self._bottom_margin: float = 0
        self._right_margin: float = 0

        self.top_margin = top_margin
        self.left_margin = left_margin
        self.bottom_margin = bottom_margin
        self.right_margin = right_margin

    @property
    def bottom_margin(self) -> float:
        return self._bottom_margin

    @bottom_margin.setter
    def bottom_margin(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='bottom_margin')
        self._bottom_margin = float(val)

    @property
    def left_margin(self) -> float:
        return self._left_margin

    @left_margin.setter
    def left_margin(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='left_margin')
        self._left_margin = float(val)

    @property
    def top_margin(self) -> float:
        return self._top_margin

    @top_margin.setter
    def top_margin(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='top_margin')
        self._top_margin = float(val)

    @property
    def right_margin(self) -> float:
        return self._right_margin

    @right_margin.setter
    def right_margin(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='right_margin')
        self._right_margin = float(val)


class Positioned:
    """
    An interface for setting and getting DrawObject's position attributes.
    """

    def __init__(self, relative_x: ConvertibleToFloat = 0, relative_y: ConvertibleToFloat = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._relative_x: float = 0
        self._relative_y: float = 0

        self.relative_x = relative_x
        self.relative_y = relative_y

    @property
    def relative_x(self) -> float:
        return self._relative_x

    @relative_x.setter
    def relative_x(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='relative_x')
        self._relative_x = float(val)

    @property
    def relative_y(self) -> float:
        return self._relative_y

    @relative_y.setter
    def relative_y(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='relative_y')
        self._relative_y = float(val)


class DrawObject(ABC, Positioned, Margined):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._show: bool = True
        self._clipping_area: ClippingArea = ClippingArea(pdf=None, draw_object=self)

    @property
    def clipping_area(self) -> 'ClippingArea':
        return self._clipping_area

    @property
    def show(self) -> bool:
        return self._show

    @show.setter
    def show(self, val: bool) -> None:
        if not isinstance(val, bool):
            raise TypeError(f"show.value must be of type bool not {type(val)}")
        self._show = val

    @abstractmethod
    def get_relative_x2(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def get_relative_y2(self) -> float:
        raise NotImplementedError()

    def get_height(self) -> float:
        return self.top_margin + self.get_relative_y2() - self.relative_y + self.bottom_margin

    def get_width(self) -> float:
        return self.left_margin + self.get_relative_x2() - self.relative_x + self.right_margin

    @abstractmethod
    def draw(self, pdf: Pdf) -> None:
        raise NotImplementedError()

    def clipped_draw(self, pdf: Pdf) -> None:
        self.clipping_area.pdf = pdf
        self.clipping_area.draw()

    def get_relative_position(self) -> dict:
        return {'relative_x': self.relative_x, 'relative_y': self.relative_y}

    def get_margins(self) -> dict:
        return {'left_margin': self.left_margin, 'top_margin': self.top_margin, 'right_margin': self.right_margin,
                'bottom_margin': self.bottom_margin}


class ClippingArea:
    def __init__(self, pdf: Optional[Pdf], draw_object: DrawObject, left_margin: float = 0, right_margin: float = 0, top_margin: float = 0):
        self.pdf: Optional[Pdf] = pdf
        self.draw_object: DrawObject = draw_object
        self.left_margin: float = left_margin
        self.right_margin: float = right_margin
        self.top_margin: float = top_margin

    # private methods
    def _add_page(self) -> None:
        self.pdf.add_page()
        self._prepare_page()

    def _draw_with_clip(self, index: int) -> None:
        with self.pdf.saved_state():
            self.pdf.clip_rect(-1, -5, self.get_row_width() + 1.14, self.get_row_height())
            self.pdf.translate(index * -self.get_row_width(), 0)
            self.draw_object.draw(self.pdf)

    def _prepare_page(self) -> None:
        self.pdf.translate_page_margins()
        self.pdf.translate(self.left_margin, self.top_margin)

    # public methods
    def draw(self) -> None:
        self.pdf.translate(self.left_margin, self.top_margin)
        for index in range(self.get_number_of_rows()):
            if index != 0:
                self.pdf.translate(0, self.draw_object.get_height())
            if self.pdf.absolute_y > self.pdf.h - self.pdf.b_margin:
                self._add_page()
            self._draw_with_clip(index)

    def get_number_of_rows(self) -> int:
        return int(ceil(self.draw_object.get_width() / self.get_row_width()))

    def get_row_height(self) -> float:
        if not self.pdf:
            msg = create_error_message(class_name=self.__class__.__name__, method_name='get_row_height',
                                       argument_name=None, message='set pdf first!')
            raise PdfAttributeError(msg)
        return self.draw_object.get_height()

    def get_row_width(self) -> float:
        if not self.pdf:
            raise AttributeError('set pdf first!')
        return self.pdf.w - self.pdf.l_margin - self.pdf.r_margin - self.left_margin - self.right_margin
