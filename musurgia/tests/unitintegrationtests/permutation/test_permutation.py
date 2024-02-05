from unittest import TestCase

import pytest

from musurgia.permutation.permutation import permute


class TestFunctions(TestCase):
    def test_permute(self):
        with pytest.raises(ValueError):
            permute(None, [3, 2, 4, 1])
        with pytest.raises(ValueError):
            permute([10, 20, 30, 40], None)
        with pytest.raises(ValueError):
            permute([10, 20, 30, 40], [3, 2, 4])
        with pytest.raises(ValueError):
            permute([10, 20, 30, 40], [3, 2, 4, 5])
        with pytest.raises(ValueError):
            permute([10, 20, 30, 40], [3, 2, 4, 1, 3])
        # assert permute([10, 20, 30, 40], [3, 2, 4, 1]) == [30, 20, 40, 10]
