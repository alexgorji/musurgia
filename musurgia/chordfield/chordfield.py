from itertools import chain

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord

from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.chordfield.valuegenerator import ValueGenerator, ValueGeneratorGroup


class BreatheException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ChordFieldException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NoNextChordError(ChordFieldException):
    def __init__(self, *args):
        super().__init__(*args)


class LongEndingError(ChordFieldException):
    def __init__(self, delta, *args):
        msg = 'delta={}'.format(delta)
        super().__init__(msg, *args)


class ShortEndingError(ChordFieldException):
    def __init__(self, delta, *args):
        msg = 'delta={}'.format(delta)
        super().__init__(msg, *args)


class ChordField(object):
    """duration_ or midi_ or chord_generator can be iterators or classes with call method which use current time
    position to output a value. If a value_generator has a duration attribute, it will be overwritten by Field.duration. The same is
    the case for sum (s) in ArithmeticProgression """

    def __init__(self, quarter_duration=None, duration_generator=None, midi_generator=None, chord_generator=None,
                 long_ending_mode=None, short_ending_mode=None, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._quarter_duration = None
        self._current_duration = None
        self._position = 0
        self._duration_generator = None
        self._midi_generator = None
        self._chord_generator = None
        self._long_ending_mode = None
        self._short_ending_mode = None
        self._exit = False
        self._first = True
        self._chords = []
        self.quarter_duration = quarter_duration
        self.duration_generator = duration_generator
        self.midi_generator = midi_generator
        self.chord_generator = chord_generator
        self.long_ending_mode = long_ending_mode
        self.short_ending_mode = short_ending_mode
        self.name = name
        self.parent_group = None

    def _set_value_generator_duration(self, value_generator):
        if value_generator is not None:
            if isinstance(value_generator, ArithmeticProgression):
                value_generator.s = self.quarter_duration
            else:
                try:
                    value_generator.duration = self.quarter_duration
                except AttributeError:
                    pass

    @property
    def quarter_duration(self):
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, value):
        if value is not None:
            self._quarter_duration = value
            self._set_value_generator_duration(self.duration_generator)
            self._set_value_generator_duration(self.midi_generator)
            self._set_value_generator_duration(self.chord_generator)

    @property
    def duration_generator(self):
        return self._duration_generator

    @duration_generator.setter
    def duration_generator(self, value):
        self._duration_generator = value
        self._set_value_generator_duration(self.duration_generator)

    @property
    def midi_generator(self):
        return self._midi_generator

    @midi_generator.setter
    def midi_generator(self, value):
        self._midi_generator = value
        self._set_value_generator_duration(self.midi_generator)

    @property
    def chord_generator(self):
        return self._chord_generator

    @chord_generator.setter
    def chord_generator(self, value):
        self._chord_generator = value
        if value:
            self._set_value_generator_duration(self.chord_generator)

    @property
    def long_ending_mode(self):
        return self._long_ending_mode

    @long_ending_mode.setter
    def long_ending_mode(self, value):
        """
        :param value: can be None, pre, post
        for dealing with last chord, if it is too long and ends after self.quarter_duration
        None: last chord will be cut short.
        pre: last chord will be omitted and self.quarter_duration cut short.
        post: self.quarter_duration will be prolonged.
        """
        permitted = [None, 'pre', 'post']
        if value not in permitted:
            raise ValueError('{} not in permitted long_ending_modes: {}'.format(value, permitted))
        self._long_ending_mode = value

    @property
    def short_ending_mode(self):
        return self._short_ending_mode

    @short_ending_mode.setter
    def short_ending_mode(self, value):
        """

        :param value: can be None, rest and prolong
        for dealing with last chord, if it is too short and ends before self.quarter_duration
        None: self.quarter_duration will be cut short.
        rest: a rest with remaining quarter_duration will be added.
        prolong: last chord will be prolonged
        """
        permitted = [None, 'rest', 'prolong']
        if value not in permitted:
            raise ValueError('{} not in permitted short_ending_mode: {}'.format(value, permitted))
        self._short_ending_mode = value

    @property
    def position(self):
        return self._position

    @property
    def position_in_group(self):
        if self.parent_group:
            index = self.parent_group.fields.index(self)
            if index == 0:
                return 0
            else:
                return sum([chord_field.quarter_duration for chord_field in self.parent_group.fields[:index]])
        else:
            return None

    def _get_next_duration(self):
        if self.duration_generator:
            try:
                return self.duration_generator.__next__()
            except AttributeError:
                return self.duration_generator(self.position)
        elif self.parent_group and self.parent_group.duration_generator:
            try:
                return self.parent_group.duration_generator.__next__()
            except AttributeError:
                return self.parent_group.duration_generator(self.position + self.position_in_group)
        else:
            return 1

    def _get_next_midi(self):
        if self.midi_generator:
            try:
                return self.midi_generator.__next__()
            except AttributeError:
                return self.midi_generator(self.position)
        elif self.parent_group and self.parent_group.midi_generator:
            try:
                return self.parent_group.midi_generator.__next__()
            except AttributeError:
                return self.parent_group.midi_generator(self.position + self.position_in_group)
        else:
            return 71

    def __iter__(self):
        return self

    def __next__(self):
        if self.quarter_duration == 0:
            raise StopIteration()

        if self._exit:
            raise StopIteration()

        if self.chord_generator is None:
            next_duration = self._get_next_duration()
            next_midi = self._get_next_midi()

            remain = self.quarter_duration - self.position
            self._position += next_duration

            if self._position < self.quarter_duration:
                pass
            elif self._position == self.quarter_duration:
                self._exit = True

            elif self._position > self.quarter_duration:
                if self.long_ending_mode is None:
                    next_duration = remain
                    self._position = self.quarter_duration
                elif self.long_ending_mode == 'post':
                    self.quarter_duration = self.position
                elif self.long_ending_mode == 'pre':
                    self.quarter_duration = self.position - remain
                    raise StopIteration()

                self._exit = True
            chord = TreeChord(quarter_duration=next_duration, midis=next_midi)
            if self._first:
                if self.name is not None:
                    chord.add_lyric(self.name)
                self._first = False

            self._chords.append(chord)
            return chord
        else:
            try:
                next_chord = self.chord_generator(self.position)
            except TypeError:
                next_chord = self.chord_generator.__next__()
            remain = self.quarter_duration - self.position
            self._position += next_chord.duration
            if self._position < self.quarter_duration:
                pass
            elif self._position == self.quarter_duration:
                self._exit = True
            elif self._position > self.quarter_duration:
                if self.long_ending_mode is None:
                    next_chord.quarter_duration = remain
                    self._position = self.quarter_duration
                elif self.long_ending_mode == 'post':
                    self.quarter_duration = self.position
                elif self.long_ending_mode == 'pre':
                    self.quarter_duration = self.position - remain

                self._exit = True

            if self._first:
                if self.name is not None:
                    next_chord.add_lyric(self.name)
                self._first = False
            self._chords.append(next_chord)
            return next_chord

    @property
    def chords(self):
        list(self)
        delta = self.quarter_duration - sum([chord.quarter_duration for chord in self._chords])
        if delta > 0:
            if self.short_ending_mode is None:
                self._quarter_duration -= delta
            elif self.short_ending_mode == 'rest':
                self._chords.append(TreeChord(midis=0, quarter_duration=delta))
            else:
                self._chords[-1].quarter_duration += delta
        return self._chords

    @property
    def simple_format(self):
        sf = SimpleFormat()
        for chord in self.chords:
            sf.add_chord(chord)
        return sf


class ChordField2(object):
    def __init__(self, quarter_duration=None, duration_generator=None, midi_generator=None, chord_generator=None,
                 long_ending_mode=None, short_ending_mode=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._quarter_duration = None
        self._duration_generator = None
        self._midi_generator = None
        self._chord_generator = None
        self._chords = None
        self._long_ending_mode = None
        self._short_ending_mode = None
        self._children = None
        self._parent = None
        # self._current_duration = None
        # self._position = 0
        # self._exit = False
        # self._first = True

        self.quarter_duration = quarter_duration
        self.duration_generator = duration_generator
        self.midi_generator = midi_generator
        self.chord_generator = chord_generator
        self.long_ending_mode = long_ending_mode
        self.short_ending_mode = short_ending_mode

        # self.name = name
        # self.parent_group = None

    def _get_value_generators(self):
        return [value_generator for value_generator in
                (self.chord_generator, self.duration_generator, self.midi_generator) if value_generator is not None]

    def _set_up_value_generator(self, value_generator, value_mode=None):
        if not isinstance(value_generator, ValueGenerator) and not isinstance(value_generator, ValueGeneratorGroup):
            raise TypeError('value_generator must be of type ValueGenerator or ValueGeneratorGroup not {}'.format(
                type(value_generator)))
        value_generator.value_mode = value_mode

        if isinstance(value_generator, ValueGenerator):
            value_generator.duration = self.quarter_duration
        elif isinstance(value_generator, ValueGeneratorGroup):
            if value_generator.duration != 0:
                factor = self.quarter_duration / value_generator.duration
                for vg in value_generator.value_generators:
                    vg.duration *= factor
            else:
                raise ValueError('value_generator of type ValueGeneratorGroup cannot have 0 duration')

    @property
    def children(self):
        return self._children

    def add_child(self, child):
        if not isinstance(child, ChordField2):
            raise TypeError()
        if self._children is None:
            self._children = []

        self._children.append(child)
        if child.duration_generator:
            if self.duration_generator is None:
                self.duration_generator = ValueGenerator()
                self.duration_generator.add_child(child.duration_generator)
            elif self.duration_generator.children:
                self.duration_generator.add_child(child.duration_generator)
            else:
                pass
        if child.midi_generator:
            if self.midi_generator is None:
                self.midi_generator = ValueGenerator()
                self.midi_generator.add_child(child.midi_generator)
            elif self.midi_generator.children:
                self.midi_generator.add_child(child.midi_generator)
            else:
                pass
        if child.chord_generator:
            if self.chord_generator is None:
                self.chord_generator = ValueGenerator()
                self.chord_generator.add_child(child.chord_generator)
            elif self.chord_generator.children:
                self.chord_generator.add_child(child.chord_generator)
            else:
                pass

        self._parent = self

    @property
    def quarter_duration(self):
        if self.children:
            children_quarter_durations = [child.quarter_duration for child in self.children]
            if None in children_quarter_durations:
                return None
            else:
                return sum(children_quarter_durations)
        return self._quarter_duration

    @quarter_duration.setter
    def quarter_duration(self, value):
        if value is not None:
            if self.children:
                raise ChordFieldException('parents quarter_duration cannot be set')
            self._quarter_duration = value
            for value_generator in self._get_value_generators():
                self._set_up_value_generator(value_generator, value_generator.value_mode)

    @property
    def duration_generator(self):
        return self._duration_generator

    @duration_generator.setter
    def duration_generator(self, value):
        self._duration_generator = value
        if value:
            self._set_up_value_generator(self.duration_generator, 'duration')

    @property
    def midi_generator(self):
        return self._midi_generator

    @midi_generator.setter
    def midi_generator(self, value):
        self._midi_generator = value
        if value:
            self._set_up_value_generator(self.midi_generator, 'midi')

    @property
    def chord_generator(self):
        return self._chord_generator

    @chord_generator.setter
    def chord_generator(self, value):
        self._chord_generator = value
        if value:
            self._set_up_value_generator(self.chord_generator, 'chord')

    @property
    def position_in_duration(self):
        if self.duration_generator:
            if isinstance(self.duration_generator, ValueGenerator):
                return self.duration_generator.position_in_duration
            else:
                return self.duration_generator.position_in_duration
        elif self.chord_generator:
            return self.chord_generator.position_in_duration
        else:
            return None

    @property
    def long_ending_mode(self):
        return self._long_ending_mode

    @long_ending_mode.setter
    def long_ending_mode(self, val):
        """
        :param val: can be None, 'self_extend', 'cut', 'omit', 'omit_and_add_rest', 'omit_and_stretch'
        for dealing with last chord, if it is too long and ends after self.quarter_duration
        None: raises Error
        self_extend: self.quarter_duration will be prolonged.
        cut: last chord will be cut short.
        omit: last chord will be omitted and self.quarter_duration cut short.
        omit_and_add_rest: last chord will be omitted and rests will be added.
        omit_and_stretch: last chord will be omitted and the new last chord  will be extended.
        """
        permitted = [None, 'self_extend', 'cut', 'omit', 'omit_and_add_rest', 'omit_and_stretch']
        if val not in permitted:
            raise ValueError('long_ending_mode.value {} must be in {}'.format(val, permitted))
        self._long_ending_mode = val

    @property
    def short_ending_mode(self):
        return self._short_ending_mode

    @short_ending_mode.setter
    def short_ending_mode(self, val):
        """
        :param val: can be None, 'self_shrink', 'add_rest', 'stretch'
        for dealing with last chord, if it is too long and ends after self.quarter_duration
        None: raises Error
        self_shrink: self.quarter_duration will be shortened.
        omit: rests will be added.
        stretch: last chord will be prolonged.
        """
        permitted = [None, 'self_shrink', 'add_rest', 'stretch']
        if val not in permitted:
            raise ValueError('short_ending_mode.value {} must be in {}'.format(val, permitted))
        self._short_ending_mode = val

    @property
    def chords(self):
        return self._chords

    @property
    def simple_format(self):
        sf = SimpleFormat()
        list(self)
        for chord in self.chords:
            sf.add_chord(chord)
        return sf

    def _get_next_duration(self):
        if self.duration_generator:
            return self.duration_generator.__next__()
        else:
            return None

    def _get_next_midi(self):
        if self.midi_generator:
            self.midi_generator.position_in_duration = self.position_in_duration
            return self.midi_generator.__next__()
        else:
            return None

    def _get_next_chord(self):
        next_chord = None
        next_midi = self._get_next_midi()
        next_duration = self._get_next_duration()

        if self.chord_generator:
            next_chord = self.chord_generator.__next__()

        if next_chord:
            if next_duration:
                next_chord.quarter_duration = next_duration
            if next_midi:
                next_chord.midis = next_midi
        else:
            if not next_duration:
                raise NoNextChordError('no chord_ and duration_generator')
            if not next_midi:
                raise NoNextChordError('no chord_ and midi_generator')
            next_chord = TreeChord(quarter_duration=next_duration, midis=next_midi)
        if self._chords is None:
            self._chords = []
        self._chords.append(next_chord)
        return next_chord

    def _check_quarter_duration(self):
        delta = sum([chord.quarter_duration for chord in self.chords]) - self.quarter_duration

        if delta > 0:
            if self.long_ending_mode == 'self_extend':
                self.quarter_duration += delta
            elif self.long_ending_mode == 'cut':
                self.chords[-1].quarter_duration -= delta
            elif self.long_ending_mode in ['omit', 'omit_and_add_rest', 'omit_and_stretch']:
                self.chords.pop()
                new_delta = self.quarter_duration - sum([chord.quarter_duration for chord in self.chords])
                if self.long_ending_mode == 'omit_and_add_rest':
                    self.chords.append(TreeChord(midis=0, quarter_duration=new_delta))
                elif self.long_ending_mode == 'omit_and_stretch':
                    self.chords[-1].quarter_duration += new_delta
                else:
                    self.quarter_duration -= new_delta
            else:
                raise LongEndingError(delta)

        elif delta < 0:
            if self.short_ending_mode == 'self_shrink':
                self.quarter_duration += delta
            elif self.short_ending_mode == 'add_rest':
                self.chords.append(TreeChord(midis=0, quarter_duration=-delta))
            elif self.short_ending_mode == 'stretch':
                self.chords[-1].quarter_duration -= delta
            else:
                raise ShortEndingError(delta)
        else:
            pass

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self._get_next_chord()
        except StopIteration:
            self._check_quarter_duration()
            raise StopIteration()


class ChordFieldGroup(object):
    def __init__(self, duration_generator=None, midi_generator=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._duration_generator = None
        self._midi_generator = None
        self._field_iter = None
        self._fields = []
        self._current_field = None
        self._chords = []
        self.duration_generator = duration_generator
        self.midi_generator = midi_generator

    @property
    def fields(self):
        return self._fields

    def _set_value_generator_duration(self, value_generator):
        if value_generator is not None:
            if isinstance(value_generator, ArithmeticProgression):
                value_generator.s = self.get_duration()
            else:
                try:
                    value_generator.duration = self.get_duration()
                except AttributeError:
                    pass

    @property
    def duration_generator(self):
        try:
            self._set_value_generator_duration(self._duration_generator)
        except AttributeError:
            pass
        return self._duration_generator

    @duration_generator.setter
    def duration_generator(self, val):
        self._duration_generator = val

    @property
    def midi_generator(self):
        try:
            self._set_value_generator_duration(self._midi_generator)
        except AttributeError:
            pass
        return self._midi_generator

    @midi_generator.setter
    def midi_generator(self, val):
        self._midi_generator = val
        # self._set_value_generator_duration(self.midi_generator)

    def get_duration(self):
        if self.fields:
            return sum([field.quarter_duration for field in self.fields])
        else:
            return 0

    def add_field(self, field):
        if field is None:
            field = ChordField()
        if not isinstance(field, ChordField):
            raise TypeError('{} has wrong type for Field'.format(field))
        else:
            field.parent_group = self
            self._fields.append(field)
            if not self._field_iter:
                self._field_iter = iter(self.fields)
            else:
                self._field_iter = chain(self._field_iter, field)
        return field

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_field is None:
            self._current_field = self._field_iter.__next__()
        try:
            chord = self._current_field.__next__()
            self._chords.append(chord)
            return chord
        except StopIteration:
            self._current_field = self._field_iter.__next__()
            self.__next__()

    @property
    def chords(self):
        list(self)
        return self._chords

    @property
    def simple_format(self):
        sf = SimpleFormat()
        for chord in self.chords:
            sf.add_chord(chord)
        return sf


class Breathe(ChordFieldGroup):
    def __init__(self, quarter_durations, breakpoints=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._quarter_durations = []
        self._breakpoints = []
        self.quarter_durations = quarter_durations
        self.breakpoints = breakpoints

    @property
    def quarter_durations(self):
        return [self.repose_1.quarter_duration, self.inspiration.quarter_duration, self.climax.quarter_duration,
                self.expiration.quarter_duration, self.repose_2.quarter_duration]

    @quarter_durations.setter
    def quarter_durations(self, values):
        if not self._quarter_durations:
            if len(values) != 5:
                ValueError('quarter_durations must have 5 elements.')
            self._fields = []
            names = ['repose_1', 'inspiration', 'climax', 'expiration', 'repose_2']
            for index, quarter_duration in enumerate(values):
                field = ChordField(quarter_duration=quarter_duration)
                field.name = names[index]
                self.add_field(field)
                self._quarter_durations.append(quarter_duration)
        else:
            raise BreatheException('quarter_durations can only be set during initialisation')

    @property
    def breakpoints(self):
        return self._breakpoints

    @breakpoints.setter
    def breakpoints(self, values):
        if not self._breakpoints:
            if len(values) != 3:
                ValueError('quarter_durations must have 3 elements.')
            for i in range(5):
                if i == 0:
                    a1, an = values[0], values[0]
                elif i == 1:
                    a1, an = values[0], values[1]
                elif i == 2:
                    a1, an = values[1], values[1]
                elif i == 3:
                    a1, an = values[1], values[2]
                elif i == 4:
                    a1, an = values[2], values[2]
                self.fields[i].duration_generator = ArithmeticProgression(a1=a1, an=an, correct_s=True)
        else:
            raise BreatheException('breakpoints can only be set during initialisation')

    @property
    def repose_1(self):
        return self.fields[0]

    @property
    def inspiration(self):
        return self.fields[1]

    @property
    def climax(self):
        return self.fields[2]

    @property
    def expiration(self):
        return self.fields[3]

    @property
    def repose_2(self):
        return self.fields[4]
