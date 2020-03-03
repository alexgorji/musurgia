from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord

from musurgia.arithmeticprogression import ArithmeticProgression
from musurgia.chordfield.valuegenerator import ValueGenerator, ValueGeneratorGroup, ValueGeneratorException


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
        msg = 'delta={}'.format(float(delta))
        super().__init__(msg, *args)


class ShortEndingError(ChordFieldException):
    def __init__(self, delta, *args):
        msg = 'delta={}'.format(float(delta))
        super().__init__(msg, *args)


class ParentSetQuarterDurationError(ChordFieldException):
    def __init__(self, *args):
        msg = 'parent\'s quarter_duration cannot be set'
        super().__init__(msg, *args)


class ChordField(object):
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
        self._position = 0
        self._name = None

        self.quarter_duration = quarter_duration
        self.duration_generator = duration_generator
        self.midi_generator = midi_generator
        self.chord_generator = chord_generator
        self.long_ending_mode = long_ending_mode
        self.short_ending_mode = short_ending_mode

    def _get_value_generators(self):
        return [value_generator for value_generator in
                (self.chord_generator, self.duration_generator, self.midi_generator) if value_generator is not None]

    def _set_up_value_generator(self, value_generator, value_mode=None):
        if not isinstance(value_generator, ValueGenerator) and not isinstance(value_generator, ValueGeneratorGroup):
            raise TypeError('value_generator must be of type ValueGenerator or ValueGeneratorGroup not {}'.format(
                type(value_generator)))
        value_generator.value_mode = value_mode
        value_generator.duration = self.quarter_duration

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    def add_child(self, child):
        if not isinstance(child, ChordField):
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
        child._parent = self
        self._update_durations()

    def _update_durations(self):
        for value_generator in self._get_value_generators():
            try:
                value_generator.duration = self.quarter_duration
            except ValueGeneratorException:
                pass

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
                raise ParentSetQuarterDurationError()
            else:
                self._quarter_duration = value
                self._update_durations()
                if self.parent:
                    self.parent._update_durations()

    @property
    def duration_generator(self):
        if not self._duration_generator and self.parent and self.parent.duration_generator:
            return self.parent.duration_generator
        return self._duration_generator

    @duration_generator.setter
    def duration_generator(self, value):
        self._duration_generator = value
        if value:
            self._set_up_value_generator(self.duration_generator, 'duration')

    @property
    def midi_generator(self):
        if not self._midi_generator and self.parent and self.parent.midi_generator:
            return self.parent.midi_generator
        return self._midi_generator

    @midi_generator.setter
    def midi_generator(self, value):
        self._midi_generator = value
        if value:
            self._set_up_value_generator(self.midi_generator, 'midi')

    @property
    def chord_generator(self):
        if not self._chord_generator and self.parent:
            return self.parent.chord_generator
        return self._chord_generator

    @chord_generator.setter
    def chord_generator(self, value):
        self._chord_generator = value
        if value:
            self._set_up_value_generator(self.chord_generator, 'chord')

    @property
    def position(self):
        return self._position

    @property
    def position_in_parent(self):
        index = self.parent.children.index(self)
        if index == 0:
            return 0
        return sum([child.quarter_duration for child in self.parent.children[:index]])

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
        list(self)
        sf = SimpleFormat()
        for chord in self.chords:
            sf.add_chord(chord)
        return sf

    def _get_next_duration(self):
        if self.duration_generator:
            next_duration = self.duration_generator.__next__()
            self._position += next_duration
            return next_duration
        else:
            return None

    def _get_next_midi(self):
        if self.midi_generator:
            # if not self.duration_generator and not self.chord_generator:
            #     raise ChordFieldException('set duration_generator or chord_generator first')
            self.midi_generator.position = self.position
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
                try:
                    self.quarter_duration += delta
                except ParentSetQuarterDurationError:
                    self.children[-1].quarter_duration += delta
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
            next_chord = self._get_next_chord()
            return next_chord
        except StopIteration:
            self._check_quarter_duration()
            raise StopIteration()


class Breathe(ChordField):
    def __init__(self, proportions, breakpoints=None, quarter_duration=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._proportions = None
        self._breakpoints = None
        self.proportions = proportions
        self.breakpoints = breakpoints
        self.quarter_duration = quarter_duration

    @property
    def quarter_durations(self):
        return [self.repose_1.quarter_duration, self.inspiration.quarter_duration, self.climax.quarter_duration,
                self.expiration.quarter_duration, self.repose_2.quarter_duration]

    def _generate_children(self, quarter_duration):
        names = ['repose_1', 'inspiration', 'climax', 'expiration', 'repose_2']
        fields = []
        for index, proportion in enumerate(self.proportions):
            child_quarter_duration = proportion * quarter_duration / sum(self.proportions)
            field = ChordField(quarter_duration=child_quarter_duration)
            field.name = names[index]
            fields.append(field)

        if not self.breakpoints:
            self.breakpoints = [0.25, 1, 0.25]

        for i in range(5):
            if i == 0:
                a1, an = self.breakpoints[0], self.breakpoints[0]
            elif i == 1:
                a1, an = self.breakpoints[0], self.breakpoints[1]
            elif i == 2:
                a1, an = self.breakpoints[1], self.breakpoints[1]
            elif i == 3:
                a1, an = self.breakpoints[1], self.breakpoints[2]
            else:
                a1, an = self.breakpoints[2], self.breakpoints[2]
            fields[i].duration_generator = ValueGenerator(ArithmeticProgression(a1=a1, an=an, correct_s=True))
        for field in fields:
            self.add_child(field)

    @ChordField.quarter_duration.setter
    def quarter_duration(self, value):
        if value is not None:
            self._generate_children(value)

    @property
    def proportions(self):
        return self._proportions

    @proportions.setter
    def proportions(self, values):
        if not self._proportions:
            if len(values) != 5:
                ValueError('quarter_durations must have 5 elements.')
            self._proportions = values
        else:
            raise BreatheException('proportions can only be set during initialisation')

    @property
    def breakpoints(self):
        return self._breakpoints

    @breakpoints.setter
    def breakpoints(self, values):
        if not self._breakpoints:
            if len(values) != 3:
                ValueError('quarter_durations must have 3 elements.')
            self._breakpoints = values
        else:
            raise BreatheException('breakpoints can only be set during initialisation')

    @property
    def repose_1(self):
        return self.children[0]

    @property
    def inspiration(self):
        return self.children[1]

    @property
    def climax(self):
        return self.children[2]

    @property
    def expiration(self):
        return self.children[3]

    @property
    def repose_2(self):
        return self.children[4]
