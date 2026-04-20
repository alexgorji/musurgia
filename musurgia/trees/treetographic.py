from decimal import Decimal
from typing import Any, Mapping


from musurgia.graphics.container import Container
from musurgia.graphics.geometry import LineOrientation, Position, Scalar


from musurgia.graphics.segmented_line import SegmentedLine
from musurgia.trees.valuedtree import ValuedTree
from musurgia.utils import convert_fraction_to_decimal


__all__ = ["TreeGraphicFactory"]


class TreeGraphicFactory:
    def __init__(
        self,
        valued_tree: ValuedTree,
        unit: int = 1,
        marker_length: Scalar = 10,
        default_layer_bottom_margin=5,
        shrink_factor: Decimal = Decimal("0.7"),
        options: dict[int, dict[int, Mapping[str, Any]]] | None = None,
        **kwargs,
    ) -> None:
        self._valued_tree: ValuedTree = valued_tree
        self._unit = unit
        self._marker_length = marker_length
        self._default_layer_bottom_margin = default_layer_bottom_margin
        self._shrink_factor = shrink_factor
        self._options = options
        self._kwargs = kwargs

    def _create_layer_segmented_line(self, layer_number: int) -> SegmentedLine:
        segment_lengths = self._valued_tree.get_layer(
            layer_number,
            key=lambda n: convert_fraction_to_decimal(n.get_value() * self._unit),
        )
        options = self._options.get(layer_number) if self._options else None
        layer_segmented_line = SegmentedLine(
            type=LineOrientation.HORIZONTAL,
            segment_lengths=segment_lengths,
            marker_length=self._get_marker_length(layer_number),
            options=options,
            **self._kwargs,
        )
        return layer_segmented_line

    def _get_marker_length(self, layer_number: int) -> Decimal:
        return (self._shrink_factor / layer_number) * self._marker_length

    def create(self) -> Container:
        container = Container()
        y = 0
        for layer_number in range(1, self._valued_tree.get_number_of_layers() + 1):
            sl = self._create_layer_segmented_line(layer_number)
            container.add_draw_object(Position(0, y), sl)
            y += sl.size.height + self._default_layer_bottom_margin
            print(y)
        return container
