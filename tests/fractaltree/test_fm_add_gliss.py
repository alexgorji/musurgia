import os
from unittest import TestCase

from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):

    def test_1(self):
        fm = FractalMusic(tempo=60, quarter_duration=10)
        fm.midi_generator.midi_range = [60, 72]
        fm.add_layer()
        for child in fm.get_children():
            child.add_gliss()
        score = fm.get_score(show_fractal_orders=True, layer_number=fm.number_of_layers)
        xml_path = path + '_test_1.xml'
        score.write(path=xml_path)
