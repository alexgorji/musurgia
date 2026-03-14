from dataclasses import dataclass
from typing import Any, List

from musurgia.graphics.drawobject import Container, Position, TextDrawObject


@dataclass
class Label:
    text: str
    offset: Position = Position(0, 0)


class LabeledMixin:
    def __init__(self, *, labels=None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._labels: list[Label] = labels or []
        self._build()

    def get_labels(self) -> List[Label]:
        return self._labels

    def _build(self) -> None:
        if not isinstance(self, Container):
            raise TypeError()
        for label in self._labels:
            self.add_draw_object(label.offset, TextDrawObject(text=label.text))
