from abc import ABC, abstractmethod

from musurgia.pdf.margined import Margined
from musurgia.pdf.positioned import Positioned


class DrawObject(ABC, Positioned, Margined):
    def __init__(self, show=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._show = None
        self._page_break = False
        self._line_break = False
        self._parent = None
        self.show = show

    @property
    def parent(self):
        return self._parent

    def _check_line_break(self, pdf):
        next_x2 = pdf.x + self.get_relative_x2()
        printable_range = pdf.w - pdf.r_margin
        diff = next_x2 - printable_range
        if diff > 0:
            self._line_break = True
            self.relative_x -= printable_range
            if self.relative_x < 0:
                self.relative_x = 0

            if self.parent:
                bottom_margin = self.parent.bottom_margin
            else:
                bottom_margin = self.bottom_margin
            pdf.y += self.get_relative_y2() + bottom_margin
            # pdf.y += self.get_relative_y2()
            pdf.x = pdf.l_margin

    def _check_page_break(self, pdf):
        next_y2 = pdf.y + self.get_relative_y2() + self.bottom_margin
        printable_y_range = pdf.h - pdf.b_margin
        diff = next_y2 - printable_y_range
        if diff > 0:
            self._page_break = True
            # self.relative_y -= printable_y_range
            # if self.relative_y < 0:
            #     self.relative_y = 0

            margins = pdf.l_margin, pdf.t_margin, pdf.r_margin, pdf.b_margin
            pdf.add_page()
            pdf.l_margin, pdf.t_margin, pdf.r_margin, pdf.b_margin = margins
            # if self.parent:
            #     top_margin = self.parent.top_margin
            # else:
            #     top_margin = self.top_margin
            # pdf.y = pdf.t_margin + top_margin
            pdf.y = pdf.t_margin
            pdf.x = pdf.l_margin

    @abstractmethod
    def get_relative_x2(self):
        raise NotImplementedError()

    @abstractmethod
    def get_relative_y2(self):
        raise NotImplementedError()

    def get_height(self):
        return self.get_relative_y2() - self.relative_y

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
