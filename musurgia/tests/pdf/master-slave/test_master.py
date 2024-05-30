from musurgia.pdf.masterslave import Master, PositionedMaster, MarginedMaster
from musurgia.tests._test_utils import PdfTestCase


class DummyMaster(Master):

    def get_slave_position(self, slave, position):
        pass

    def get_slave_margin(self, slave, margin):
        pass


class DummyPositionMaster(PositionedMaster):
    def get_slave_position(self, slave, position):
        pass


class DummyMarginMaster(MarginedMaster):
    def get_slave_margin(self, slave, margin):
        pass


class TestMaster(PdfTestCase):
    def test_init(self):
        m = DummyMaster()
        self.assertTrue(isinstance(m, Master))

    def test_init_margin(self):
        m = DummyMarginMaster()
        self.assertTrue(isinstance(m, MarginedMaster))

    def test_init_position(self):
        m = DummyPositionMaster()
        self.assertTrue(isinstance(m, PositionedMaster))
