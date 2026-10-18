from decimal import Decimal

from musurgia.graphics.container import Container
from musurgia.graphics.geometry import LineOrientation, Position, Scalar
from musurgia.graphics.segmented_line import LineSegment, SegmentedLine
from musurgia.trees.valuetree import ValueTree
from musurgia.utils import dToX


def _convert_layer_node_values_to_scaled_decimal(
    nodes: list[ValueTree], scale: Scalar
) -> list[Decimal]:
    positions = [
        Decimal(p.numerator) * scale / Decimal(p.denominator)
        for p in dToX([node.get_value() for node in nodes])
    ]
    return [end - start for start, end in zip(positions, positions[1:])]


def _convert_layer_to_segmented_line(
    nodes: list[ValueTree], scale: Scalar
) -> SegmentedLine:
    lengths = _convert_layer_node_values_to_scaled_decimal(nodes, scale)
    sl = SegmentedLine(
        type=LineOrientation.HORIZONTAL,
        line_segments=[
            LineSegment(type=LineOrientation.HORIZONTAL, length=length)
            for length in lengths
        ],
    )
    sl.get_line_segments()[-1].add_end_maker()
    return sl


class ValueTreeGraphic:
    def __init__(
        self,
        tree: ValueTree,
        scale: Scalar = 1,
        distance_between_layers: Scalar = 10,
        *args: str,
        **kwarg: str,
    ) -> None:
        self._tree = tree
        self._scale = scale
        self.distance_between_layers = distance_between_layers
        self._layers: list[SegmentedLine] = self._create_layers()
        self._is_built = False
        super().__init__(*args, **kwarg)

    @property
    def scale(self) -> Scalar:
        return self._scale

    @property
    def tree(self) -> ValueTree:
        return self._tree

    def _create_layers(self) -> list[SegmentedLine]:
        layers = [
            self.tree.get_layer(n + 1) for n in range(self.tree.get_number_of_layers())
        ]
        return [_convert_layer_to_segmented_line(layer, self.scale) for layer in layers]

    def build(self) -> Container:
        if self._is_built:
            raise RuntimeError("This graphic has already been built.")
        for layer in self._layers:
            layer.build()
        container = Container()
        for index, layer in enumerate(self._layers):
            container.add_draw_object(
                position=Position(0, index * self.distance_between_layers),
                draw_object=layer,
            )
        self._is_built = True
        return container
