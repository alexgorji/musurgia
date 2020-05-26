from fpdf import FPDF
from fpdf.php import sprintf

from musurgia.pdf.line import HorizontalSegmentedLine, VerticalSegmentedLine
from musurgia.pdf.pdfunit import PdfUnit
from musurgia.pdf.text import PageText, TextLabel


class PageNumber(PageText):
    def __init__(self, value='none', v_position='center', h_position='bottom', *args, **kwargs):
        super().__init__(value=value, v_position=v_position, h_position=h_position, *args, **kwargs)

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


class PrepareDrawObject:
    def __init__(self, pdf, draw_object):
        self.pdf = pdf
        self.draw_object = draw_object

    def __enter__(self):
        self.pdf._push_state()
        self.pdf.translate(self.draw_object.relative_x, self.draw_object.relative_y)
        self.pdf.translate(self.draw_object.left_margin, self.draw_object.top_margin)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pdf._pop_state()


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

        self.set_font("Helvetica", "", 10)

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

    @property
    def k(self):
        return PdfUnit.get_k()

    @k.setter
    def k(self, val):
        pass

    def add_space(self, val):
        self.y += val

    def add_page(self):
        super().add_page(orientation=self.cur_orientation)

    def prepare_draw_object(self, draw_object):
        pdo = PrepareDrawObject(self, draw_object=draw_object)
        return pdo

    def reset_font(self):
        self._out(sprintf('BT /F%d %.2f Tf ET',
                          self.current_font['i'],
                          self.font_size_pt))

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

    def translate_page_margins(self):
        self.translate(self.l_margin, self.t_margin)

    def draw_ruler(self, mode='h', unit=10, first_label=0, show_first_label=False, label_show_interval=1,
                   label_attribute_function=None):
        if mode in ['h', 'horizontal']:
            number_of_units = (self.w - self.l_margin - self.r_margin) / unit
        elif mode in ['v', 'vertical']:
            number_of_units = (self.h - self.t_margin - self.b_margin) / unit
        else:
            raise AttributeError()

        partial_segment_length = number_of_units - int(number_of_units)
        lengths = int(number_of_units) * [unit]
        if partial_segment_length:
            lengths += [partial_segment_length * unit]
        if mode in ['h', 'horizontal']:
            ruler = HorizontalSegmentedLine(lengths)
        else:
            ruler = VerticalSegmentedLine(lengths)

        if partial_segment_length:
            ruler.segments[-1].end_mark_line.show = False
        for index, segment in enumerate(ruler.segments):
            if not show_first_label and index == 0:
                pass
            else:
                if index % label_show_interval == 0:
                    tl = TextLabel(index + first_label)
                    if mode in ['v', 'vertical']:
                        tl.placement = 'left'
                        tl.right_margin = 1
                        tl.top_margin = 1
                    else:
                        tl.bottom_margin = 1
                    if label_attribute_function:
                        label_attribute_function(tl)
                    segment.start_mark_line.add_text_label(tl)

        with self.saved_state():
            ruler.draw(self)

    def write(self, path):
        if self.show_page_number:
            self.draw_page_number()
        self.output(path, 'F')
