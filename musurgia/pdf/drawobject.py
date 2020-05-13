from abc import ABC, abstractmethod

from musurgia.pdf.margined import Margined
from musurgia.pdf.positioned import Positioned


class DrawObject(ABC, Positioned, Margined):
    def __init__(self, show=True, bottom_margin=10, *args, **kwargs):
        super().__init__(bottom_margin=bottom_margin, *args, **kwargs)
        self._show = None
        self._page_break = False
        self._line_break = False
        self.show = show

    def _check_line_break(self, pdf):
        next_x2 = pdf.x + self.get_relative_x2()
        printable_range = pdf.w - pdf.r_margin
        diff = next_x2 - printable_range
        if diff > 0:
            self._line_break = True
            self.relative_x -= printable_range
            if self.relative_x < 0:
                self.relative_x = 0

            pdf.y += self.get_relative_y2()
            pdf.x = pdf.l_margin

    def _check_page_break(self, pdf):
        next_y2 = pdf.y + self.get_relative_y2()
        printable_y_range = pdf.h - pdf.b_margin
        diff = next_y2 - printable_y_range
        if diff > 0:
            self._page_break = True
            self.relative_y -= printable_y_range
            if self.relative_y < 0:
                self.relative_y = 0

            margins = pdf.l_margin, pdf.t_margin, pdf.r_margin, pdf.b_margin
            pdf.add_page()
            pdf.l_margin, pdf.t_margin, pdf.r_margin, pdf.b_margin = margins

            pdf.y = pdf.t_margin
            pdf.x = pdf.l_margin

    @abstractmethod
    def get_relative_x2(self):
        raise NotImplementedError()

    @abstractmethod
    def get_relative_y2(self):
        raise NotImplementedError()

    @abstractmethod
    def draw(self, pdf):
        raise NotImplementedError()

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, val):
        if not isinstance(val, bool):
            raise TypeError()
        self._show = val

    def draw_with_break(self, pdf):
        self._check_line_break(pdf)
        self._check_page_break(pdf)
        self.draw(pdf)
