from musurgia.arithmeticprogression import ArithmeticProgression


class ValueGeneratorException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class GeneratorIsNotCallable(ValueGeneratorException):
    def __init__(self, generator, *args):
        msg = 'generator {} is not callable.'.format(generator)
        super().__init__(msg, *args)


class XOutOfRange(ValueGeneratorException):
    def __init__(self, *args):
        super().__init__(*args)


class NoneDuration(ValueGeneratorException):
    def __init__(self, *args):
        super().__init__(*args)


class ValueGeneratorTypeConflict(ValueGeneratorException):
    def __init__(self, *args):
        super().__init__(*args)


class ValueGenerator(object):
    def __init__(self, generator, duration, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._generator = None
        self._duration = None
        self._position_in_group = 0

        self.generator = generator
        self.duration = duration

    @property
    def generator(self):
        return self._generator

    @generator.setter
    def generator(self, val):
        raise NotImplementedError('generator must be overwritten')

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
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, val):
        self._duration = val
        if val is not None:
            self._set_generator_duration()

    @property
    def position_in_group(self):
        return self._position_in_group

class IterableValueGenerator(ValueGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @ValueGenerator.generator.setter
    def generator(self, val):
        if not hasattr(val, '__iter__'):
            raise TypeError('generator of IterableValueGenerator must be iterable')
        else:
            self._generator = val

    def __next__(self):
        return self.generator.__next__()

    def __iter__(self):
        return self


class CallableValueGenerator(ValueGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @ValueGenerator.generator.setter
    def generator(self, val):
        if not callable(val):
            raise TypeError('generator of CallableValueGenerator must be callable')
        else:
            self._generator = val

    def __call__(self, x):
        if self.duration is None:
            raise NoneDuration('CallableValueGenerator needs a None value duration')

        minimum = self.position_in_group
        maximum = minimum + self.duration
        if minimum <= x < maximum:
            return self.generator.__call__(x - self.position_in_group)
        else:
            raise XOutOfRange('x: {} must be in range ({} - {})'.format(x, minimum, maximum))


class ValueGeneratorGroup(object):
    def __init__(self, *value_generators, **kwargs):
        super().__init__(**kwargs)
        self._value_generators = None
        self.value_generators = value_generators
        self._child_type = None

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
    def quarter_duration(self):
        try:
            return [vg.quarter_duration for vg in self.value_generators]
        except AttributeError:
            return None

    def add_value_generator(self, value_generator):
        if not isinstance(value_generator, ValueGenerator):
            raise TypeError('value_generators must be of type ValueGenerator not{}'.format(type(value_generator)))
        if self._value_generators is None:
            self._value_generators = []
            if isinstance(value_generator, IterableValueGenerator):
                self._child_type = IterableValueGenerator
            else:
                self._child_type = CallableValueGenerator
        else:
            if not isinstance(value_generator, self._child_type):
                raise ValueGeneratorTypeConflict()
        self._value_generators.append(value_generator)
