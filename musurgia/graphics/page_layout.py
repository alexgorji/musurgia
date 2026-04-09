from dataclasses import dataclass, field
from typing import Dict, Literal


from musurgia.graphics.geometry import Margins, Size


type PageSize = Literal["A3", "A4", "A5"]
type PageOrientation = Literal["portrait", "landscape"]


PAGE_SIZES: Dict[PageSize, Size] = {
    "A5": Size(148, 210),
    "A4": Size(210, 297),
    "A3": Size(297, 420),
}


@dataclass(frozen=True)
class PageLayout:
    size: PageSize | Size = "A4"
    orientation: PageOrientation = "portrait"
    margins: Margins = field(default_factory=lambda: Margins(0, 0, 0, 0))

    def get_size(self) -> Size:
        if isinstance(self.size, Size):
            return self.size
        size = PAGE_SIZES[self.size]
        if self.orientation == "landscape":
            return Size(size.height, size.width)
        return size

    def get_effective_size(self) -> Size:
        t, r, b, l = self.margins.to_values()
        return Size(
            self.get_size().width - r - l,
            self.get_size().height - b - t,
        )
