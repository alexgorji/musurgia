from pathlib import Path

from musurgia.pdf.line import HorizontalSegmentedLine, VerticalSegmentedLine
from musurgia.pdf.masterslave import PositionMaster
from musurgia.pdf.pdf import Pdf
from musurgia.pdf.text import TextLabel
from musurgia.unittest import TestCase

path = Path(__file__)


class DummyPositionMaster(PositionMaster):
    def get_slave_position(self, slave, position):
        if position == 'x':
            return 10
        elif position == 'y':
            return 20


class TestTextLabel(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_draw(self):
        t = TextLabel(master=DummyPositionMaster(), name='t1', text='Fox is going to be dead.')

        with self.file_path(path, 'draw', 'pdf') as pdf_path:
            with self.pdf.saved_state():
                HorizontalSegmentedLine(10 * [10]).draw(self.pdf)
            with self.pdf.saved_state():
                VerticalSegmentedLine(10 * [10]).draw(self.pdf)
            t.draw(self.pdf)
            self.pdf.write(pdf_path)

    def test_draw_multiple(self):
        t1 = TextLabel(master=DummyPositionMaster(), name='t1', text='Fox is going to be dead.')
        t2 = TextLabel(master=DummyPositionMaster(), name='t2', text='What should we do??')
        t3 = TextLabel(master=DummyPositionMaster(), name='t3', text='What should we do??')
        with self.file_path(path, 'draw_multiple', 'pdf') as pdf_path:
            with self.pdf.saved_state():
                HorizontalSegmentedLine(10 * [10], relative_y=1.5).draw(self.pdf)
            with self.pdf.saved_state():
                VerticalSegmentedLine(10 * [10]).draw(self.pdf)
            t1.draw(self.pdf)
            t2.draw(self.pdf)
            t3.draw(self.pdf)
            self.pdf.write(pdf_path)
    #
    # def test_draw_with_top_margin(self):
    #     t = Text('fox is going to be dead.')
    #     t.top_margin = 2
    #     with self.file_path(path, 'draw_with_top_margin', 'pdf') as pdf_path:
    #         t.draw(self.pdf)
    #         self.pdf.write(pdf_path)
