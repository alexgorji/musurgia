from pathlib import Path

from musurgia.pdf.pdf import Pdf
from musurgia.timeline.timeline import TimeLine
from musurgia.unittest import TestCase, create_path

path = Path(__file__)


class Test(TestCase):
    def setUp(self) -> None:
        self.pdf = Pdf()

    def test_time_line_with_voices(self):
        pdf_path = create_path(path, 'time_line_with_voices.pdf')
        tl = TimeLine(length=200)
        voice = tl.add_voice(name='v 1')
        # for line_segment in voice.line_segments:
        #     print(line_segment.)
        tl.draw(self.pdf)
        self.pdf.write(pdf_path)
