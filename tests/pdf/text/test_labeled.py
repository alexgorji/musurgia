from musurgia.pdf.labeled import Labeled
from musurgia.pdf.margined import Margined
from musurgia.pdf.positioned import Positioned
from musurgia.unittest import TestCase


class DummyLabeled(Positioned, Margined, Labeled):
    pass


class TestLabeled(TestCase):
    def test_above_labels_height(self):
        dl = DummyLabeled()
        tl1 = dl.add_text_label('first')
        tl2 = dl.add_text_label('second')
        actual = dl.get_above_labels_height()
        expected = 10.308166666666665
        self.assertAlmostEqual(expected, actual)
