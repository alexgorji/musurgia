import copy

from musurgia.pdf.font import Font
from musurgia.pdf.newdrawobject import DrawObject


class Text(DrawObject):
    DEFAULT_FONT_FAMILY = 'Arial'
    DEFAULT_FONT_SIZE = 10
    DEFAULT_FONT_WEIGHT = 'regular'
    DEFAULT_FONT_STYLE = 'regular'

    def __init__(self, text, pdf_k=float(72 / 25.4), font_family=None, font_weight=None, font_style=None,
                 font_size=None, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.font = Font()
        self.font_family = font_family
        self.font_weight = font_weight
        self.font_style = font_style
        self.font_size = font_size
        self._text = None
        self._pdf_k = None
        self.text = text
        self.pdf_k = pdf_k

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
    def pdf_k(self):
        return self._pdf_k

    @pdf_k.setter
    def pdf_k(self, val):
        if not isinstance(val, float):
            raise TypeError(f"pdf_k.value must be of type float not{type(val)}")
        self._pdf_k = val

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val):
        self._text = str(val)

    def _set_default_top_margin(self):
        self.top_margin = self.get_relative_y2() - self.relative_y

    def get_relative_x2(self):
        return self.relative_x + self.font.get_approximate_text_pixel_width(self.text) * self.pdf_k

    def get_relative_y2(self):
        return self.relative_y + self.font.get_text_pixel_height() * self.pdf_k

    def draw(self, pdf):
        if self.top_margin is None:
            self._set_default_top_margin()
        self.pdf_k = pdf.k
        if self.show:
            style = ""
            pdf.set_font(self.font.family, style=style, size=0)
            if self.font.style == 'italic':
                style += 'I'
            if self.font.weight == 'bold':
                style += 'B'
            pdf.set_font(self.font.family, style=style, size=self.font_size)

            pdf.translate(self.relative_x, self.relative_y)
            with pdf.add_margins(self):
                pdf.text(x=2, y=2, txt=self.text)

    def __deepcopy__(self, memodict=None):
        copied = self.__class__(text=self.text)
        for var in vars(self):
            copied_var = copy.deepcopy(vars(self)[var])
            copied.__setattr__(var, copied_var)
        return copied


class TextLabel(Text):
    def __init__(self, text, placement, *args, **kwargs):
        super().__init__(text=text, *args, **kwargs)
        self._placement = None
        self.placement = placement

    @property
    def placement(self):
        return self._placement

    @placement.setter
    def placement(self, val):
        permitted = ['above', 'below']
        if val not in permitted:
            raise ValueError(f'placement.value {val} must be in {permitted}')
        self._placement = val

    def draw(self, pdf):
        super().draw(pdf)


class PageText(Text):
    def __init__(self, text, v_position=None, h_position=None, *args, **kwargs):
        super().__init__(text=text, *args, **kwargs)
        self.v_position = v_position
        self.h_position = h_position

    def get_text_physical_length(self):
        return (len(self.text)) * self.font_size / 6

    def draw(self, pdf):
        old_x, old_y = pdf.x, pdf.y
        if self.v_position == 'center':
            pdf.x = (pdf.w / 2) - self.get_text_physical_length() / 2
        elif self.v_position == 'left':
            pdf.x = pdf.l_margin
        elif self.v_position == 'right':
            pdf.x = pdf.w - pdf.r_margin - self.get_text_physical_length()
        else:
            pass

        if self.h_position == 'top':
            pdf.y = pdf.t_margin
        elif self.h_position == 'bottom':
            pdf.y = pdf.h - pdf.b_margin
        else:
            pass
        super().draw(pdf)
        pdf.x, pdf.y = old_x, old_y
