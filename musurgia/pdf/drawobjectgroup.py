from musurgia.pdf.drawobject import DrawObject


class DrawObjectGroup(DrawObject):
    def __init__(self, inner_distance=None, *args, **kwargs):
        self._draw_objects = []
        self._inner_distance = 0
        self.inner_distance = inner_distance
        super().__init__(*args, **kwargs)

    def _set_inner_distances(self):
        if self.draw_objects:
            for draw_object in self.draw_objects[:-1]:
                draw_object.bottom_margin = self.inner_distance
            self.draw_objects[-1].bottom_margin = 0

    def _add_draw_object(self, draw_object):
        if not isinstance(draw_object, DrawObject):
            raise TypeError()

        self._draw_objects.append(draw_object)
        self._set_inner_distances()
        return draw_object

    def add_draw_object(self, draw_object):
        return self._add_draw_object(draw_object)

    @DrawObject.relative_x.setter
    def relative_x(self, val):
        self._relative_x = val
        try:
            for draw_object in self.draw_objects:
                draw_object.relative_x = self.relative_x
        except AttributeError:
            pass

    @DrawObject.relative_y.setter
    def relative_y(self, val):
        self._relative_y = val
        for draw_object in self.draw_objects:
            draw_object.relative_y = self.relative_y

    @property
    def draw_objects(self):
        return self._draw_objects

    @property
    def inner_distance(self):
        return self._inner_distance

    @inner_distance.setter
    def inner_distance(self, val):
        self._inner_distance = val
        self._set_inner_distances()

    def get_relative_x2(self):
        if self.draw_objects:
            return max([do.get_relative_x2() for do in self.draw_objects])
        else:
            return None

    def get_relative_y2(self):
        if self.draw_objects:
            return sum([do.get_relative_y2() + do.bottom_margin for do in self.draw_objects]) + self.relative_y
        else:
            return None

    def draw(self, pdf):
        old_pdf_x = pdf.x
        old_pdf_page = pdf.page
        new_top_margin = 0
        for draw_object in self.draw_objects:
            # print(f'top_margin:{new_top_margin}')
            draw_object.top_margin = new_top_margin
            old_pdf_y = pdf.y
            old_bottom_margin = draw_object.bottom_margin

            draw_object.bottom_margin = self.get_height() + self.bottom_margin - draw_object.get_height()

            pdf.page = old_pdf_page
            pdf.x = old_pdf_x

            draw_object.draw(pdf)

            draw_object.bottom_margin = old_bottom_margin
            new_top_margin = draw_object.get_relative_y2() + draw_object.bottom_margin
            pdf.y = old_pdf_y + draw_object.get_height() + draw_object.bottom_margin

        pdf.y += self.bottom_margin
