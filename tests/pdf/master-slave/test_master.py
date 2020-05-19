from musurgia.pdf.masterslave import Master
from musurgia.unittest import TestCase


class DummyMaster(Master):
    def get_slave_margin(self, slave, margin):
        pass

    def get_slave_position(self, slave, position):
        pass


class TestMaster(TestCase):
    def test_init(self):
        m = DummyMaster()
        self.assertTrue(isinstance(m, Master))
