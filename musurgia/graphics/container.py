import copy
import logging

from musurgia.graphics.drawobject import (
    Coordinates,
    DrawObject,
    Position,
    Size,
)


from typing import Literal, overload

logger = logging.getLogger(__name__)


class ClippingArea:
    def __init__(
        self, start: Position, width: int | float, height: int | float
    ) -> None:
        self._start: Position = start
        self._width: int | float = width
        self._height: int | float = height

    def clip(self, container: "Container") -> "Container":
        clipped_container = Container()
        for p, do in container.get_draw_objects(positioned=True):
            new_p = self._get_new_position(p)
            if self._drawobject_is_inside_area(p, do):
                clipped_container.add_draw_object(new_p, copy.deepcopy(do))
            elif not isinstance(do, Container):
                clipped = do.clip(self._start, self._width, self._height)
                if not clipped:
                    logger.warning(
                        f"Non clippable drawobject {do} has been omitted from clipping area."
                    )
                else:
                    clipped_container.add_draw_object(new_p, clipped)
            else:
                raise NotImplementedError
        return clipped_container

    def _get_end(self) -> Position:
        return self._start + Position.from_values(self._width, self._height)

    def _get_new_position(self, position: Position) -> Position:
        return position - self._start

    def _drawobject_is_inside_area(
        self, position: Position, drawobject: DrawObject
    ) -> bool:
        if position.x < self._start.x or position.y < self._start.y:
            return False
        if (
            position.x + drawobject.size.width > self._get_end().x
            or position.y + drawobject.size.height > self._get_end().y
        ):
            return False
        return True


class Container(DrawObject):
    def __init__(self) -> None:
        super().__init__()
        self._positioned_draw_objects: list[tuple[Position, DrawObject]] = []
        self._clipping_area: ClippingArea | None = None

    def _get_clipping_area_height(
        self, start: Position, height: None | int | float
    ) -> int | float:
        max_height = self.size.height - start.y
        if max_height <= 0:
            raise AttributeError("Invalid start value: ", start)
        if height is not None:
            if height <= 0:
                raise AttributeError("Invalid height value: ", height)
            if height <= max_height:
                return height
        return max_height

    def _get_clipping_area_width(
        self, start: Position, width: None | int | float
    ) -> int | float:
        max_width = self.size.width - start.x
        if max_width <= 0:
            raise AttributeError("Invalid start value: ", start)
        if width is not None:
            if width <= 0:
                raise AttributeError("Invalid width value: ", width)
            if width <= max_width:
                return width
        return max_width

    def add_draw_object(
        self, position: Position, draw_object: DrawObject
    ) -> "Container":
        self._positioned_draw_objects.append((position, draw_object))
        return self

    def clip(
        self,
        start: Position = Position(0, 0),
        width: int | float | None = None,
        height: int | float | None = None,
    ) -> "Container":
        width = self._get_clipping_area_width(start=start, width=width)
        height = self._get_clipping_area_height(start=start, height=height)
        clipping_area = ClippingArea(start, width, height)
        return clipping_area.clip(self)

    @overload
    def get_draw_objects(self) -> list[DrawObject]: ...

    @overload
    def get_draw_objects(self, *, recursive: bool) -> list[DrawObject]: ...

    @overload
    def get_draw_objects(self, *, positioned: Literal[False]) -> list[DrawObject]: ...

    @overload
    def get_draw_objects(
        self, *, positioned: Literal[False], recursive: bool
    ) -> list[DrawObject]: ...

    @overload
    def get_draw_objects(
        self, *, positioned: Literal[True]
    ) -> list[tuple[Position, DrawObject]]: ...

    @overload
    def get_draw_objects(
        self, *, positioned: Literal[True], recursive: bool
    ) -> list[tuple[Position, DrawObject]]: ...

    def get_draw_objects(
        self, *, recursive: bool = False, positioned: bool = False
    ) -> list[DrawObject] | list[tuple[Position, DrawObject]]:
        if not positioned:
            if recursive:
                return_value = []
                for _, o in self._positioned_draw_objects:
                    if not isinstance(o, Container):
                        return_value.append(o)
                    else:
                        return_value.extend(
                            [
                                oo
                                for _, oo in o._get_positioned_draw_objects(
                                    recursive=True
                                )
                            ]
                        )
                return return_value

            return [o for _, o in self._positioned_draw_objects]
        else:
            return self._get_positioned_draw_objects(recursive=recursive)

    def _get_positioned_draw_objects(
        self, recursive: bool = False
    ) -> list[tuple[Position, DrawObject]]:
        if recursive:
            return_value = []
            for p, o in self._positioned_draw_objects:
                if not isinstance(o, Container):
                    return_value.append((p, o))
                else:
                    return_value.extend(
                        [
                            (p + pp, oo)
                            for pp, oo in o._get_positioned_draw_objects(recursive=True)
                        ]
                    )
            return return_value

        return self._positioned_draw_objects

    @property
    def size(self) -> Size:
        coor = self.get_bounding_box_coordinates()
        return Size(coor.tr.x - coor.tl.x, coor.bl.y - coor.tl.y)

    def get_bounding_box_coordinates(self) -> Coordinates:
        tl, tr, br, bl = [
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
        ]
        for p, d in self._get_positioned_draw_objects():
            coor = d.get_bounding_box_coordinates()
            if coor.tl.x + p.x < tl[0]:
                tl[0] = coor.tl.x + p.x
            if coor.tl.y + p.y < tl[1]:
                tl[1] = coor.tl.y + p.y
            if coor.tr.x + p.x > tr[0]:
                tr[0] = coor.tr.x + p.x
            if coor.tr.y + p.y < tr[1]:
                tr[1] = coor.tr.y + p.y
            if coor.br.x + p.x > br[0]:
                br[0] = coor.br.x + p.x
            if coor.br.y + p.y > br[1]:
                br[1] = coor.br.y + p.y
            if coor.bl.x + p.x < bl[0]:
                bl[0] = coor.bl.x + p.x
            if coor.bl.y + p.y > bl[1]:
                bl[1] = coor.bl.y + p.y

        return Coordinates(
            Position.from_values(*tl),
            Position.from_values(*tr),
            Position.from_values(*br),
            Position.from_values(*bl),
        )
