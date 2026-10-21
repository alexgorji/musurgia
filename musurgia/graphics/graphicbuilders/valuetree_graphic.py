from decimal import Decimal
from fractions import Fraction

from verysimpletree import HomogeneousTree


from musurgia.graphics.container import Container
from musurgia.graphics.geometry import LineOrientation, Position, Scalar
from musurgia.graphics.segmented_line import Label, LineSegment, SegmentedLine
from musurgia.trees.valuetree import ValueTree
from musurgia.utils import dToX
from typing import TypedDict


def _convert_layer_node_values_to_scaled_decimal(
    nodes: list[ValueTree], scale: Scalar
) -> list[Decimal]:
    positions = [
        Decimal(p.numerator) * scale / Decimal(p.denominator)
        for p in dToX([node.get_value() for node in nodes])
    ]
    return [end - start for start, end in zip(positions, positions[1:])]


class TreeGraphicOptions(TypedDict):
    scale: Scalar
    distance_between_layers: Scalar
    marker_max_length: Scalar
    marker_length_shrinking_factor: Scalar
    marker_max_thickness: Scalar
    marker_thickness_shrinking_factor: Scalar


class TreeGraphicOptionsPatch(TypedDict, total=False):
    scale: Scalar
    distance_between_layers: Scalar
    marker_max_length: Scalar
    marker_length_shrinking_factor: Scalar
    marker_max_thickness: Scalar
    marker_thickness_shrinking_factor: Scalar


DEFAULT_TREE_GRAPHIC_OPTIONS: TreeGraphicOptions = {
    "scale": 10,
    "distance_between_layers": 10,
    "marker_max_length": 10,
    "marker_length_shrinking_factor": Decimal("0.7"),
    "marker_max_thickness": Decimal("0.5"),
    "marker_thickness_shrinking_factor": Decimal("0.7"),
}


class ValueTreeGraphic(HomogeneousTree):
    def __init__(
        self,
        value_tree_node: ValueTree,
        *,
        options: TreeGraphicOptionsPatch | None = None,
        **kwarg: str,
    ) -> None:
        super().__init__(**kwarg)
        self._value_tree_node = value_tree_node
        self._line_segment: LineSegment | None = None
        self._options: TreeGraphicOptions | None = None
        self.options = options
        self._populate()
        self._is_built = False

    @property
    def options(self) -> TreeGraphicOptions:
        if self.is_root:
            if not self._options:
                self._options = DEFAULT_TREE_GRAPHIC_OPTIONS.copy()
            return self._options
        return self.get_root().options

    @options.setter
    def options(self, value: TreeGraphicOptionsPatch | None) -> None:
        if value and not self.is_root:
            raise ValueError("Only root accepts options.")
        self._options = DEFAULT_TREE_GRAPHIC_OPTIONS.copy()
        if value:
            self._options.update(value)

    def _populate(self) -> None:
        for v_node in self.get_value_tree_node().get_children():
            self.add_child(ValueTreeGraphic(v_node))
        if self.get_value_tree_node().is_root:
            for layer in self.get_layers()[:-1]:
                for node in layer:
                    if node.is_leaf:
                        node.add_child(ValueTreeGraphic(node.get_value_tree_node()))

            marker_lengths = {Fraction(0): self.options["marker_max_length"]}
            marker_thicknesses = {Fraction(0): self.options["marker_max_thickness"]}

            for index, layer in enumerate(self.get_layers()):
                lengths = _convert_layer_node_values_to_scaled_decimal(
                    [node.get_value_tree_node() for node in layer],
                    self.options["scale"],
                )
                positions = dToX(lengths)[:-1]
                for node, length, position in zip(
                    layer, lengths, positions, strict=True
                ):
                    if position not in marker_lengths.keys():
                        marker_lengths[position] = self.options[
                            "marker_max_length"
                        ] * self.options["marker_length_shrinking_factor"] ** (
                            index - 1
                        )
                        marker_thicknesses[position] = self.options[
                            "marker_max_thickness"
                        ] * self.options["marker_thickness_shrinking_factor"] ** (
                            index - 1
                        )
                    node._line_segment = LineSegment(
                        type=LineOrientation.HORIZONTAL, length=length
                    )
                    node._line_segment.start_marker.length = marker_lengths[position]
                    node._line_segment.start_marker.options.thickness = (
                        marker_thicknesses[position]
                    )
                    if node == layer[-1]:
                        end_marker = node._line_segment.add_end_maker()
                        end_marker.length = self.options["marker_max_length"]
                        end_marker.options.thickness = self.options[
                            "marker_max_thickness"
                        ]

    def add_label(self, label: Label) -> None:
        self.get_line_segment().start_marker.add_label(label)

    def get_line_segment(self) -> LineSegment:
        if self._line_segment is None:
            raise RuntimeError("This graphic node has no line segment.")

        return self._line_segment

    def get_value_tree_node(self) -> ValueTree:
        return self._value_tree_node

    def build(self) -> Container:
        if self._is_built:
            raise RuntimeError("This graphic has already been built.")
        container = Container()
        for index, layer in enumerate(self.get_layers()[1:]):
            sl = SegmentedLine(
                type=LineOrientation.HORIZONTAL,
                line_segments=[node.get_line_segment() for node in layer],
            )
            sl.build()
            container.add_draw_object(
                position=Position(0, index * self.options["distance_between_layers"]),
                draw_object=sl,
            )
        self._is_built = True
        return container
