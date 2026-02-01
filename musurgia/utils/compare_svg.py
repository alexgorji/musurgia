import unittest


class SVGTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compareSVGToPNG(self, svg):
        return False
