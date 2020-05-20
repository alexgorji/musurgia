from pathlib import Path

import matplotlib as mpl
from matplotlib.afm import AFM

from musurgia.unittest import TestCase

afm_path = Path(mpl.get_data_path(), 'fonts', 'afm', 'ptmr8a.afm')


def make_afm_path_dictionary():
    output = {}
    directory = Path(mpl.get_data_path(), 'fonts', 'afm')
    for file in directory.iterdir():
        afm_path = file
        with afm_path.open('rb') as fh:
            with afm_path.open('rb') as fh:
                afm = AFM(fh)
            output[afm.family_name] = afm

    return output


class Test(TestCase):
    def test_afm_dict(self):
        actual = list(make_afm_path_dictionary().keys())
        expected = ['New Century Schoolbook',
                    'Times',
                    'ITC Bookman',
                    'Helvetica',
                    'ITC Avant Garde Gothic',
                    'Palatino',
                    'Computer Modern',
                    'Symbol',
                    'ITC Zapf Dingbats',
                    'Utopia',
                    'Courier',
                    'ITC Zapf Chancery']
        self.assertEqual(expected, actual)

    def test_load_afm(self):
        afm = make_afm_path_dictionary()['Times']
        actual = afm.get_familyname()
        expected = 'Times'
        self.assertEqual(expected, actual)

    def test_width_height(self):
        afm = make_afm_path_dictionary()['Helvetica']
        actual = afm.string_width_height('What the heck?')
        expected = (7370.0, 741)
        self.assertEqual(expected, actual)
