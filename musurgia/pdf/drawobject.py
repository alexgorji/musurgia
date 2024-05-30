from abc import ABC, abstractmethod
from math import ceil
from typing import Optional, Protocol, Any, cast

from musurgia.musurgia_exceptions import PdfAttributeError
from musurgia.musurgia_types import create_error_message, check_type
from musurgia.pdf.margined import AbstractMargined
from musurgia.pdf.masterslave import Slave, Master, PositionedMaster, PositionedSlave, MarginedMaster, MarginedSlave
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.positioned import AbstractPositioned


class HasGetHeightProtocol(Protocol):
    def get_height(self) -> float: ...


class DrawObject(AbstractPositioned, AbstractMargined, ABC):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._show = True
        self._clipping_area = ClippingArea(pdf=None, draw_object=self)

    @property
    def clipping_area(self) -> 'ClippingArea':
        return self._clipping_area

    @property
    def show(self) -> bool:
        return self._show

    @show.setter
    def show(self, val: bool) -> None:
        check_type(val, bool, class_name=self.__class__.__name__, property_name='show')
        self._show = val

    @abstractmethod
    def get_relative_x2(self) -> float:
        """ this property is needed to get relative_x2 """

    @abstractmethod
    def get_relative_y2(self) -> float:
        """ this property is needed to get relative_y2 """

    def get_height(self) -> float:
        return self.top_margin + self.get_relative_y2() - self.relative_y + self.bottom_margin

    def get_width(self) -> float:
        return self.left_margin + self.get_relative_x2() - self.relative_x + self.right_margin

    @abstractmethod
    def draw(self, pdf: Pdf) -> None:
        """ this property is needed draw the DrawObject to pdf """

    def clipped_draw(self, pdf: Pdf) -> None:
        self.clipping_area.pdf = pdf
        self.clipping_area.draw()


class SlaveDrawObject(DrawObject, Slave, PositionedSlave, MarginedSlave, ABC):
    pass


class MasterDrawObject(DrawObject, Master, PositionedMaster, MarginedMaster, ABC):
    pass


class ClippingArea:
    def __init__(self, pdf: Optional[Pdf], draw_object: DrawObject, left_margin: float = 0, right_margin: float = 0,
                 top_margin: float = 0):
        self.pdf: Optional[Pdf] = pdf
        self.draw_object: DrawObject = draw_object
        self.left_margin: float = left_margin
        self.right_margin: float = right_margin
        self.top_margin: float = top_margin

    # private methods
    def _add_page(self) -> None:
        if not self.pdf:
            raise PdfAttributeError(self._get_pdf_not_exists_message('_add_page'))
        self.pdf.add_page()
        self._prepare_page()

    def _get_pdf_not_exists_message(self, method_name: str) -> str:
        return create_error_message(message='pdf must be set first', class_name=self.__class__.__name__,
                                    method_name=method_name)

    def _draw_with_clip(self, index: int) -> None:
        if not self.pdf:
            raise PdfAttributeError(self._get_pdf_not_exists_message('_draw_with_clip'))
        with self.pdf.saved_state():
            self.pdf.clip_rect(-1, -5, self.get_row_width() + 1.14, self.get_row_height())
            self.pdf.translate(index * -self.get_row_width(), 0)
            self.draw_object.draw(self.pdf)

    def _prepare_page(self) -> None:
        if not self.pdf:
            raise PdfAttributeError(self._get_pdf_not_exists_message('_prepare_page'))
        self.pdf.translate_page_margins()
        self.pdf.translate(self.left_margin, self.top_margin)

    # public methods
    def draw(self) -> None:
        if not self.pdf:
            raise PdfAttributeError(self._get_pdf_not_exists_message('_prepare_page'))
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
        return self.draw_object.get_height()

    def get_row_width(self) -> float:
        if not self.pdf:
            raise PdfAttributeError(self._get_pdf_not_exists_message('_prepare_page'))
        return self.pdf.w - self.pdf.l_margin - self.pdf.r_margin - self.left_margin - self.right_margin
