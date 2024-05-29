from abc import ABC
from typing import Optional

from musurgia.musurgia_exceptions import RelativePositionNotSettableError
from musurgia.musurgia_types import check_type, LabelPlacement, FontStyle, FontFamily, FontWeight, ConvertibleToFloat, \
    VerticalPosition, HorizontalPosition
from musurgia.pdf.font import Font
from musurgia.pdf.drawobject import DrawObject
from musurgia.pdf.margined import Margined
from musurgia.pdf.pdfunit import PdfUnit
from musurgia.pdf.positioned import PositionedSlave, Positioned


class AbstractText(DrawObject, ABC):
    DEFAULT_FONT_FAMILY = 'Courier'
    DEFAULT_FONT_SIZE = 10
    DEFAULT_FONT_WEIGHT = 'medium'
    DEFAULT_FONT_STYLE = 'regular'

    def __init__(self, value, font_family: Optional[FontFamily] = None, font_weight: Optional[FontWeight] = None,
                 font_style: Optional[FontStyle] = None,
                 font_size: Optional[ConvertibleToFloat] = None, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.font = Font()
        self.font_family = font_family
        self.font_weight = font_weight
        self.font_style = font_style
        self.font_size = font_size
        self._value = None
        self.value = value

    @property
    def font_family(self):
        return self.font.family

    @font_family.setter
    def font_family(self, val):
        if val is None:
            val = self.DEFAULT_FONT_FAMILY
        self.font.family = val

    @property
    def font_size(self):
        return self.font.size

    @font_size.setter
    def font_size(self, val):
        if val is None:
            val = self.DEFAULT_FONT_SIZE
        self.font.size = val

    @property
    def font_weight(self):
        return self.font.weight

    @font_weight.setter
    def font_weight(self, val):
        if val is None:
            val = self.DEFAULT_FONT_WEIGHT
        self.font.weight = val

    @property
    def font_style(self):
        return self.font.style

    @font_style.setter
    def font_style(self, val):
        if val is None:
            val = self.DEFAULT_FONT_STYLE
        self.font.style = val

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = str(val)

    def get_text_width(self):
        return self.font.get_text_pixel_width(self.value) / PdfUnit.get_k()

    def get_text_height(self):
        return self.font.get_text_pixel_height(self.value) / PdfUnit.get_k()

    def get_relative_x2(self) -> float:
        return self.relative_x + self.get_text_width()

    def get_relative_y2(self) -> float:
        return self.relative_y + self.get_text_height()

    def draw(self, pdf):
        # if pdf.k != PdfUnit.get_k():
        #     raise AttributeError('wrong pdf.k!')
        if self.show:
            pdf.reset_font()
            style = ""
            if self.font_style == 'italic':
                style += 'I'
            if self.font_weight == 'bold':
                style += 'B'
            pdf.set_font(self.font.family, style=style, size=self.font_size)
            with pdf.prepare_draw_object(self):
                pdf.text(x=0, y=0, text=self.value)


class Text(AbstractText, Positioned, Margined):
    pass


class TextLabel(PositionedSlave, AbstractText, Margined):
    def __init__(self, value, master=None, placement: LabelPlacement = 'above', *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
        self._master = None
        self.master = master
        self._placement = None
        self.placement = placement

    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, value):
        self._master = value

    @property
    def placement(self):
        return self._placement

    @placement.setter
    def placement(self, val):
        check_type(val, 'LabelPlacement', class_name=self.__class__.__name__, property_name='placement')
        self._placement = val


class PageText(Text):
    def __init__(self, value, v_position: VerticalPosition = 'top', h_position: HorizontalPosition = 'left', *args,
                 **kwargs):
        super().__init__(value=value, *args, **kwargs)
        self._v_position = None
        self._h_position = None
        self.v_position = v_position
        self.h_position = h_position

    @Text.relative_y.setter
    def relative_y(self, val):
        if val:
            raise RelativePositionNotSettableError

    @Text.relative_x.setter
    def relative_x(self, val):
        if val:
            raise RelativePositionNotSettableError

    @property
    def v_position(self) -> VerticalPosition:
        return self._v_position

    @v_position.setter
    def v_position(self, val: VerticalPosition) -> None:
        check_type(val, 'VerticalPosition')
        self._v_position = val

    @property
    def h_position(self) -> HorizontalPosition:
        return self._h_position

    @h_position.setter
    def h_position(self, val: HorizontalPosition) -> None:
        check_type(val, 'HorizontalPosition')
        self._h_position = val

    def draw(self, pdf):
        pdf.reset_position()
        if self.h_position == 'center':
            self._relative_x = ((pdf.w - pdf.l_margin - pdf.r_margin) / 2) - self.get_width() / 2
        elif self.h_position == 'left':
            self._relative_x = pdf.l_margin
        elif self.h_position == 'right':
            self._relative_x = pdf.w - pdf.r_margin - self.get_width()
        else:
            raise NotImplementedError  # pragma: no cover

        if self.v_position == 'top':
            self._relative_y = pdf.t_margin
        elif self.v_position == 'bottom':
            self._relative_y = pdf.h - pdf.b_margin
        else:
            raise NotImplementedError  # pragma: no cover
        super().draw(pdf)
