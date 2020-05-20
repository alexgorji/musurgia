from fpdf import FPDF
from fpdf.php import sprintf

from musurgia.pdf.text import PageText


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
        self.show_page_number = False

        self.set_font("Arial", "", 10)

    def _pop_state(self):
        self._out(sprintf('Q\n'))

    def _push_state(self):
        self._out(sprintf('q\n'))

    @property
    def show_page_number(self):
        return self._show_page_number
        
    @show_page_number.setter
    def show_page_number(self, val):
        if not isinstance(val, bool):
            raise TypeError(f"show_page_number.value must be of type bool not{type(val)}")
        self._show_page_number = val
    def add_space(self, val):
        self.y += val

    def add_page(self):
        super().add_page(orientation=self.cur_orientation)

    def add_margins(self, draw_object):
        ma = AddMargins(self, draw_object=draw_object)
        return ma

    def clip_rect(self, x, y, w, h):
        x, y, w, h = x * self.k, y * self.k, w * self.k, h * self.k
        self._out(sprintf('%.2f %.2f %.2f %.2f re W n',
                          x * self.k, (self.h - y) * self.k,
                          w * self.k, -h * self.k))

    def draw_page_number(self):
        for page in self.pages:
            self.page = page
            self.page_number(page)
            self.page_number.draw(self)

    def saved_state(self):
        ss = SavedState(self)
        return ss

    def translate(self, dx, dy):
        dx, dy = dx * self.k, dy * self.k
        self._out(sprintf('1.0 0.0 0.0 1.0 %.2F %.2F cm',
                          dx, -dy))

    def translate_margins(self):
        self.translate(self.l_margin, self.t_margin)

    def write(self, path):
        if self.show_page_number:
            self.draw_page_number()
        self.output(path, 'F')
