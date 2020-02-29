from itertools import chain

from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.basic_functions import dToX


class ValueGeneratorException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class GeneratorHasNoNextError(ValueGeneratorException):
    def __init__(self, generator, *args):
        msg = 'generator {} has no __next__'.format(generator)
        super().__init__(*args)


class GeneratorNotIterableError(ValueGeneratorException):
    def __init__(self, *args):
        super().__init__(*args)


class XOutOfRange(ValueGeneratorException):
    def __init__(self, *args):
        super().__init__(*args)


class NoDurationError(ValueGeneratorException):
    def __init__(self, *args):
        super().__init__(*args)


class PositionError(ValueGeneratorException):
    def __init__(self, position_in_duration, duration, *args):
        msg = 'position_in_duration {} must be smaller than duration {}'.format(position_in_duration, duration)
        super().__init__(msg, *args)


class CallConflict(ValueGeneratorException):
    def __init__(self, *args):
        super().__init__(*args)


class ValueGeneratorTypeConflict(ValueGeneratorException):
    def __init__(self, *args):
        super().__init__(*args)


class ValueGenerator(object):
    def __init__(self, generator, value_mode=None, duration=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._generator = None
        self._duration = None
        self._position_in_duration = 0

        self.generator = generator
        self.value_mode = value_mode
        self.duration = duration

    @property
    def generator(self):
        return self._generator

    @generator.setter
    def generator(self, val):
        if not callable(val) and not hasattr(val, '__iter__'):
            raise TypeError('generator must be callable or iterable')
        self._generator = val

    def _set_generator_duration(self):
        if isinstance(self.generator, ArithmeticProgression):
            self.generator.s = self.duration
        elif hasattr(self.generator, 'quarter_duration'):
            self.generator.quarter_duration = self.duration
        elif hasattr(self.generator, 'duration'):
            self.generator.duration = self.duration
        else:
            pass

    @property
    def value_mode(self):
        return self._value_mode

    @value_mode.setter
    def value_mode(self, val):
        permitted = [None, 'duration', 'midi']
        if val not in permitted:
            raise ValueError('value_mode.value {} must be in {}'.format(val, permitted))
        self._value_mode = val

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, val):
        self._duration = val
        if val is not None and self.value_mode == 'duration':
            self._set_generator_duration()

    @property
    def position_in_duration(self):
        return self._position_in_duration

    @position_in_duration.setter
    def position_in_duration(self, val):
        if val < 0:
            raise ValueError()
        self._position_in_duration = val

    def _check_position(self):
        if not self.duration:
            raise NoDurationError()
        if not self.position_in_duration < self.duration:
            raise PositionError(self.position_in_duration, self.duration)

    def _check_value(self, value):

        self._check_position()
        if self.value_mode == 'duration':
            self.position_in_duration += value
        return value

    def __next__(self):
        if not hasattr(self.generator, '__next__'):
            if self.value_mode == 'duration':
                try:
                    return self.__call__(self.position_in_duration)
                except ValueError:
                    raise StopIteration()
            else:
                raise GeneratorHasNoNextError(self.generator)
        return self._check_value(self.generator.__next__())

    def __call__(self, x):
        self.position_in_duration = x
        if callable(self.generator):
            return self._check_value(self.generator.__call__(x))
        else:
            if isinstance(self.generator, ArithmeticProgression):
                raise CallConflict('Calling Arithmetic Progression is not allowed.')
            return self._check_value(self.generator.__next__())

    def __iter__(self):
        return self


class ValueGeneratorGroup(object):
    def __init__(self, *value_generators, **kwargs):
        super().__init__(**kwargs)
        self._value_generators = None
        self._value_generators_iterator = None
        self._child_type = None
        self._current_value_generator = None
        self.value_generators = value_generators

    @property
    def value_generators(self):
        return self._value_generators

    @value_generators.setter
    def value_generators(self, values):
        try:
            values = list(values)
        except TypeError:
            values = [values]

        for value in values:
            self.add_value_generator(value)

    @property
    def duration(self):
        try:
            return sum([vg.duration for vg in self.value_generators])
        except AttributeError:
            return None

    def add_value_generator(self, value_generator):
        if not isinstance(value_generator, ValueGenerator):
            raise TypeError('value_generators must be of type ValueGenerator not{}'.format(type(value_generator)))
        if self._value_generators is None:
            self._value_generators = []
        if self._value_generators_iterator is None:
            self._value_generators_iterator = iter([])
        value_generator.parent_group = self
        self._value_generators.append(value_generator)
        self._value_generators_iterator = chain(self._value_generators_iterator, value_generator)

    def __next__(self):
        return self._value_generators_iterator.__next__()

    def __iter__(self):
        return self

    def __call__(self, x):
        durations = [vg.duration for vg in self.value_generators]
        duration_limits = dToX(durations)
        for i in range(len(duration_limits) - 1):
            if duration_limits[i] <= x < duration_limits[i + 1]:
                return self.value_generators[i](x - duration_limits[i])
