from musurgia.pdf.newdrawobject import DrawObject
from musurgia.pdf.positioned import RelativeXNotSettableError, RelativeYNotSettableError


class RowContainer(DrawObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._draw_objects = []

    #     relative_x and y are not settable

    @property
    def draw_objects(self):
        return self._draw_objects

    @property
    def relative_x(self):
        return 0

    @relative_x.setter
    def relative_x(self):
        raise RelativeXNotSettableError()

    @property
    def relative_y(self):
        return 0

    @relative_x.setter
    def relative_y(self):
        raise RelativeYNotSettableError()

    def get_relative_x2(self):
        return sum([do.get_width() + do.left_margin + do.right_margin for do in self.draw_objects])

    def get_relative_y2(self):
        return max([do.get_relatvie_y2 + do.top_margin + do.bottom_margin for do in self.draw_objects])

    def add_draw_object(self, draw_object):
        if not isinstance(draw_object, DrawObject):
            raise TypeError()
        self._draw_objects.append(draw_object)


class Canvas(DrawObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._row_containers = []

    @property
    def row_containers(self):
        return self._row_containers

    def add_row_container(self, row_container):
        if not isinstance(row_container, RowContainer):
            raise TypeError()
        self._row_containers.append(row_container)

    def get_relative_x2(self):
        return max([rc.get_width() + rc.left_margin + rc.right_margin for rc in self.row_containers])

    def get_relative_y2(self):
        return sum([rc.get_height + rc.top_margin + rc.bottom_margin for rc in self.row_containers])

    def draw(self, pdf):
        pass
