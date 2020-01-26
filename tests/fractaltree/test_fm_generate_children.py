import os

from musurgia.agunittest import AGTestCase
from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


def _set_lyrics(fm):
    for node in fm.traverse():
        node.chord.add_lyric(str(node.fractal_order))


class Test(AGTestCase):
    def setUp(self) -> None:
        self.fm = FractalMusic(value=10)
        self.fm.tempo = 60

    def test_1(self):
        fm = self.fm
        fm.generate_children(number_of_children=0)
        _set_lyrics(fm)
        score = fm.get_score()
        xml_path = path + '_test_1.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_2(self):
        fm = self.fm
        fm.generate_children(number_of_children=1)
        _set_lyrics(fm)
        score = fm.get_score()
        xml_path = path + '_test_2.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_3(self):
        fm = self.fm
        fm.generate_children(number_of_children=2)
        _set_lyrics(fm)
        score = fm.get_score()
        xml_path = path + '_test_3.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_4(self):
        fm = self.fm
        fm.generate_children(number_of_children=3)
        _set_lyrics(fm)
        score = fm.get_score()
        xml_path = path + '_test_4.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_5(self):
        fm = self.fm
        with self.assertRaises(ValueError):
            fm.generate_children(number_of_children=4)

    def test_6(self):
        fm = self.fm
        fm.generate_children(number_of_children=(1, 1, 1))
        _set_lyrics(fm)
        score = fm.get_score()
        xml_path = path + '_test_6.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_7(self):
        fm = self.fm
        fm.generate_children(number_of_children=(0, 1, 2))
        _set_lyrics(fm)
        score = fm.get_score()
        xml_path = path + '_test_7.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_8(self):
        fm = self.fm
        fm.generate_children(number_of_children=(1, 2, (1, 2, 3)))
        _set_lyrics(fm)
        score = fm.get_score()
        xml_path = path + '_test_8.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)

    def test_9(self):
        fm = self.fm
        fm.generate_children(number_of_children=((1, 3), 2, (1, (1, 3), 3)))
        _set_lyrics(fm)
        score = fm.get_score()
        xml_path = path + '_test_9.xml'
        score.write(xml_path)
        self.assertCompareFiles(xml_path)
