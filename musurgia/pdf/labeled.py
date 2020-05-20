from abc import ABC, abstractmethod

from musurgia.pdf.masterslave import Master
from musurgia.pdf.text import TextLabel


class Labeled(ABC, Master):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._above_text_labels = []
        self._below_text_labels = []

    def add_text_label(self, val, **kwargs):
        if val is not None and not isinstance(val, TextLabel):
            val = TextLabel(val, **kwargs)
        val.parent = self
        self._text_labels.append(val)
        return val

    def add_label(self, val, **kwargs):
        return self.add_text_label(val, **kwargs)

    @property
    def text_labels(self):
        return self._text_labels

    def remove_text_labels(self):
        self._text_labels = []

    def draw_text_labels(self, pdf):
        for
