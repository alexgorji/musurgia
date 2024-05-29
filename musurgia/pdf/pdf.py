from typing import Protocol

from fpdf import FPDF, FPDF_VERSION
from musurgia.pdf.pdfunit import PdfUnit


def sprintf(fmt, *args): return fmt % args


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


class HasOutProtocol(Protocol):
    def _out(self, s): ...


class Pdf(FPDF, HasOutProtocol):
    """
    Child of fpdf.FPDF class
    """

    def __init__(self, r_margin=10, t_margin=10, l_margin=10, b_margin=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.r_margin = r_margin
        self.t_margin = t_margin
        self.l_margin = l_margin
        self.b_margin = b_margin
        self._absolute_positions = {}
        self.add_page()

        self._state = []

        self.set_font("Helvetica", "", 10)

    # private

    def _pop_state(self):
        # https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.7old.pdf
        self._state.pop()
        self._out(sprintf('Q\n'))

    def _push_state(self):
        # https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.7old.pdf
        self._state.append('push')
        self._out(sprintf('q\n'))

    # public properties
    @property
    def absolute_positions(self):
        return self._absolute_positions

    @property
    def absolute_x(self):
        return self._absolute_positions[self.page][0]

    @property
    def absolute_y(self):
        return self._absolute_positions[self.page][1]

    @property
    def k(self):
        return PdfUnit.get_k()

    @k.setter
    def k(self, val):
        pass

    # public methods

    def add_page(self):
        super().add_page(orientation=self.cur_orientation)
        self._absolute_positions[self.page] = [0, 0]

    def clip_rect(self, x, y, w, h):
        # https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.7old.pdf

        self._out(sprintf('%.2f %.2f %.2f %.2f re W n',
                          x * self.k, (self.h - y) * self.k,
                          w * self.k, -h * self.k))

    def prepare_draw_object(self, draw_object):
        return PrepareDrawObject(self, draw_object=draw_object)

    def reset_font(self):
        # https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.7old.pdf
        self._out(sprintf('BT /F%d %.2f Tf ET',
                          self.current_font['i'],
                          self.font_size_pt))

    def reset_position(self):
        self.translate(-self.absolute_x, -self.absolute_y)

    def saved_state(self):
        return SavedState(self)

    def translate(self, dx, dy):
        # https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.7old.pdf
        if not self._state:
            self._absolute_positions[self.page][0] += dx
            self._absolute_positions[self.page][1] += dy
        dx, dy = dx * self.k, dy * self.k
        self._out(sprintf('1.0 0.0 0.0 1.0 %.2F %.2F cm',
                          dx, -dy))

    def translate_page_margins(self):
        self.translate(self.l_margin, self.t_margin)

    def _putinfo(self):  # pragma: no cover
        self._out('/Producer ' + self._textstring('PyFPDF ' + FPDF_VERSION + ' http://pyfpdf.googlecode.com/'))
        if hasattr(self, 'title'):
            self._out('/Title ' + self._textstring(self.title))
        if hasattr(self, 'subject'):
            self._out('/Subject ' + self._textstring(self.subject))
        if hasattr(self, 'author'):
            self._out('/Author ' + self._textstring(self.author))
        if hasattr(self, 'keywords'):
            self._out('/Keywords ' + self._textstring(self.keywords))
        if hasattr(self, 'creator'):
            self._out('/Creator ' + self._textstring(self.creator))

    def write_to_path(self, path):
        # FPDF.close() is called inside output to write to buffer first before writing it to file.
        # print('############')
        # print('writing to path, output buffer is:', self.buffer)
        # print('')
        # print('############')
        self.output(path, 'F')
        # print('############')
        # print('written to path, output buffer is:', self.buffer)
        # print('')
        # print('############')
