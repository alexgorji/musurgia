import os

from fpdf import FPDF
from fpdf.php import sprintf

from musurgia.pdf.textlabel import Text


class PageText(Text):
    def __init__(self, text, v_position=None, h_position=None, *args, **kwargs):
        super().__init__(text=text, *args, **kwargs)
        self.v_position = v_position
        self.h_position = h_position

    def get_text_physical_length(self):
        return (len(self.text)) * self.font_size / 6

    def draw(self, pdf):
        old_x, old_y = pdf.x, pdf.y
        if self.v_position == 'center':
            pdf.x = (pdf.w / 2) - self.get_text_physical_length() / 2
        elif self.v_position == 'left':
            pdf.x = pdf.l_margin
        elif self.v_position == 'right':
            pdf.x = pdf.w - pdf.r_margin - self.get_text_physical_length()
        else:
            pass

        if self.h_position == 'top':
            pdf.y = pdf.t_margin
        elif self.h_position == 'bottom':
            pdf.y = pdf.h - pdf.b_margin
        else:
            pass
        super().draw(pdf)
        pdf.x, pdf.y = old_x, old_y


class PageNumber(PageText):
    def __init__(self, text='none', v_position='center', h_position='bottom', *args, **kwargs):
        super().__init__(text=text, v_position=v_position, h_position=h_position, *args, **kwargs)

    def __call__(self, val):
        self.text = val
        self.page = val


class SavedState:
    def __init__(self, pdf):
        self.pdf = pdf

    def __enter__(self):
        self.pdf._push_state()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pdf._pop_state()


class AddMargins:
    def __init__(self, pdf, draw_object):
        self.pdf = pdf
        self.draw_object = draw_object

    def __enter__(self):
        self.pdf.translate(self.draw_object.left_margin, self.draw_object.top_margin)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pdf.translate(self.draw_object.right_margin, self.draw_object.bottom_margin)


class Pdf(FPDF):

    def __init__(self, r_margin=10, t_margin=10, l_margin=10, b_margin=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_number = PageNumber('')
        self.r_margin = r_margin
        self.t_margin = t_margin
        self.l_margin = l_margin
        self.b_margin = b_margin
        self.add_page()

        self.set_font("Arial", "", 10)

    def add_page(self):
        super().add_page(orientation=self.cur_orientation)

    def draw_page_number(self):
        for page in self.pages:
            self.page = page
            self.page_number(page)
            self.page_number.draw(self)

    def clip_rect(self, x, y, w, h):
        x, y, w, h = x * self.k, y * self.k, w * self.k, h * self.k
        self._out(sprintf('%.2f %.2f %.2f %.2f re W n',
                          x * self.k, (self.h - y) * self.k,
                          w * self.k, -h * self.k))

    def add_space(self, val):
        self.y += val

    def saved_state(self):
        ss = SavedState(self)
        return ss

    def add_margins(self, draw_object):
        ma = AddMargins(self, draw_object=draw_object)
        return ma

    def _push_state(self):
        self._out(sprintf('q\n'))

    def _pop_state(self):
        self._out(sprintf('Q\n'))

    def translate(self, dx, dy):
        dx, dy = dx * self.k, dy * self.k
        self._out(sprintf('1.0 0.0 0.0 1.0 %.2F %.2F cm',
                          dx, -dy))

    def write(self, path):
        self.draw_page_number()
        self.output(path, 'F')
