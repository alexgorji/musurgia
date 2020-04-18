from musicscore.basic_functions import lcm, xToD


class GearWheels(object):
    def __init__(self, gear_sizes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._gear_sizes = None
        self._cycles = None
        self._iterator = None

        self.gear_sizes = gear_sizes

    # //private methods
    @staticmethod
    def _check_input(value):
        if not isinstance(value, list) or len(value) < 2:
            raise ValueError('list_of_wheels should be a list with a minimum length of 2!')
        else:
            return True

    def _set_cycles(self):
        _cycles = []
        _lcm = lcm(self.gear_sizes)
        for size in self.gear_sizes:
            number_of_cycles = (_lcm // size) + 1
            _cycles.append(range(0, number_of_cycles * size, size))
        self._cycles = _cycles

    # public properties
    @property
    def gear_sizes(self):
        return self._gear_sizes

    @gear_sizes.setter
    def gear_sizes(self, value):
        if self._check_input(value):
            self._gear_sizes = value
            self._set_cycles()
            self._iterator = iter(self.get_rhythm())

    # //public methods

    # get
    def get_cycles(self):
        return self._cycles

    def get_result(self):
        result = set(self._cycles[0])
        for cycle in self._cycles:
            result = result.union(set(cycle))
        result = list(result)
        result.sort()
        return list(result)

    def get_rhythm(self):
        return xToD(self.get_result())

    # other
    def __next__(self):
        return self._iterator.__next__()

    def __iter__(self):
        return self
