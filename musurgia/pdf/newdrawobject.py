from abc import ABC, abstractmethod

from musurgia.pdf.margined import Margined
from musurgia.pdf.positioned import Positioned


class DrawObject(ABC, Positioned, Margined):
    def __init__(self, *args, **kwargs):
        self._show = True
        self._parent = None
        super().__init__(*args, **kwargs)

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, val):
        if not isinstance(val, bool):
            raise TypeError(f"show.value must be of type bool not{type(val)}")
        self._show = val

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, val):
        self._parent = val

    @abstractmethod
    def get_relative_x2(self):
        raise NotImplementedError()

    @abstractmethod
    def get_relative_y2(self):
        raise NotImplementedError()

    def get_height(self):
        return self.top_margin + self.get_relative_y2() - self.relative_y + self.bottom_margin

    def get_width(self):
        return self.left_margin + self.get_relative_x2() - self.relative_x + self.right_margin

    @abstractmethod
    def draw(self, pdf):
        raise NotImplementedError()
