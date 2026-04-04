from musurgia.graphics.drawobject import (
    Coordinates,
    DrawObject,
    Padding,
    Position,
    Size,
)


from typing import List, Literal, Tuple, overload


class Container(DrawObject):
    def __init__(self) -> None:
        super().__init__()
        self._positioned_draw_objects: List[Tuple[Position, DrawObject]] = []
        self._padding = Padding(0, 0, 0, 0)

    def _get_padding(self) -> "Padding":
        return self._padding


    def add_draw_object(
        self, position: Position, draw_object: DrawObject
    ) -> "Container":
        self._positioned_draw_objects.append((position, draw_object))
        return self

    def clip(self, start=Position(0, 0), width=None, height=None) -> "Container":
        width = self._get_clipping_area_width(start=start, width=width)
        height = self._get_clipping_area_height(start=start, height=height)
        clipping_area = ClippingArea(start, width, height)
        print(start, width, height)
        return clipping_area.clip(self)

    @overload
    def get_draw_objects(self) -> List[DrawObject]: ...

    @overload
    def get_draw_objects(self, *, recursive: bool) -> List[DrawObject]: ...

    @overload
    def get_draw_objects(self, *, positioned: Literal[False]) -> List[DrawObject]: ...

    @overload
    def get_draw_objects(
        self, *, positioned: Literal[False], recursive: bool
    ) -> List[DrawObject]: ...

    @overload
    def get_draw_objects(
        self, *, positioned: Literal[True]
    ) -> List[Tuple[Position, DrawObject]]: ...

    @overload
    def get_draw_objects(
        self, *, positioned: Literal[True], recursive: bool
    ) -> List[Tuple[Position, DrawObject]]: ...

    def get_draw_objects(
        self, *, recursive: bool = False, positioned: bool = False
    ) -> List[DrawObject] | List[Tuple[Position, DrawObject]]:
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
    ) -> List[Tuple[Position, DrawObject]]:
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
