from musurgia.pdf.newdrawobject import DrawObject


class DrawObjectContainer(DrawObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._draw_objects = []

    def add_draw_object(self, draw_object):
        if not isinstance(draw_object, DrawObject):
            raise TypeError(draw_object)
        self._draw_objects.append(draw_object)
        return draw_object

    @property
    def draw_objects(self):
        return self._draw_objects


class DrawObjectRow(DrawObjectContainer):

    def get_relative_x2(self):
        return self.relative_x + sum([do.get_width() for do in self.draw_objects])

    def get_relative_y2(self):
        return self.relative_y + max([do.get_height() for do in self.draw_objects])

    def draw(self, pdf):
        with pdf.prepare_draw_object(self):
            for do in self.draw_objects:
                do.draw(pdf)
                pdf.translate(do.get_width(), 0)


class DrawObjectColumn(DrawObjectContainer):
    def get_relative_x2(self):
        return self.relative_x + max([do.get_width() for do in self.draw_objects])

    def get_relative_y2(self):
        return self.relative_y + sum([do.get_height() for do in self.draw_objects])

    def draw(self, pdf):
        with pdf.prepare_draw_object(self):
            for do in self.draw_objects:
                do.draw(pdf)
                pdf.translate(0, do.get_height())
