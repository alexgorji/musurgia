from musicscore.musicstream.streamvoice import SimpleFormat


class Field(object):
    def __init__(self, duration=0, duration_producer=None, midi_producer=None, note_producer=None, transition_mode=None,
                 name=None):
        self._duration = None
        self._position = 0
        self._duration_producer = None
        self._midi_producer = None
        self._note_producer = None
        self._transition_mode = None
        self._exit = False
        self._first = True
        self._simple_format = SimpleFormat()
        self.duration = duration
        self.duration_producer = duration_producer
        self.midi_producer = midi_producer
        self.note_producer = note_producer
        self.transition_mode = transition_mode
        self.name = name

    '''duration_ or midi_producers can be iterators or classes with call which use current time position to output a value. If a producer has a duration attribute, it will be overwritten by Field.duration. The same is the case for sum (s) in ArithmetichProgression'''

    def _set_producer_duration(self, producer):
        if self.duration != None and producer != None:
            # print 'set duration of ', producer
            try:
                producer.duration = self.duration
            except:
                try:
                    producer.s = self.duration
                except:
                    pass

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value
        if value != None:
            self._set_producer_duration(self.duration_producer)
            self._set_producer_duration(self.midi_producer)
            self._set_producer_duration(self.note_producer)

    @property
    def duration_producer(self):
        return self._duration_producer

    @duration_producer.setter
    def duration_producer(self, value):
        if value == None:
            value = Cycle([1])
        self._duration_producer = value
        self._set_producer_duration(self.duration_producer)

    @property
    def midi_producer(self):
        return self._midi_producer

    @midi_producer.setter
    def midi_producer(self, value):
        if value == None:
            value = Cycle([71])
        self._midi_producer = value
        self._set_producer_duration(self.midi_producer)

    @property
    def note_producer(self):
        return self._note_producer

    @note_producer.setter
    def note_producer(self, value):
        self._note_producer = value
        if value != None:
            self._set_producer_duration(self.note_producer)

    @property
    def transition_mode(self):
        return self._transition_mode

    @transition_mode.setter
    def transition_mode(self, value):
        if value not in [None, 'pre', 'post']:
            raise ValueError('transition_mode can only be None, pre or post')
        self._transition_mode = value

    @property
    def position(self):
        return self._position

    def __iter__(self):
        return self

    def next(self):

        result = None

        if self.duration == 0:
            raise StopIteration()

        if self._exit == True:
            raise StopIteration()

        try:
            if self.note_producer == None:

                if callable(getattr(self.duration_producer, 'next', None)):
                    next_duration = self.duration_producer.next()
                elif hasattr(self.duration_producer, '__call__'):
                    next_duration = self.duration_producer(self.position)

                if callable(getattr(self.midi_producer, 'next', None)):
                    next_midi = self.midi_producer.next()
                elif hasattr(self.midi_producer, '__call__'):
                    next_midi = self.midi_producer(self.position)

                remain = self.duration - self.position
                self._position += next_duration

                if self._position < self.duration:
                    result = (next_duration, next_midi)

                elif self._position == self.duration:
                    self._exit = True
                    result = (next_duration, next_midi)

                elif self._position > self.duration:
                    if self.transition_mode == None:
                        next_duration = remain
                        self._position = self.duration
                    elif self.transition_mode == 'post':
                        self.duration = self.position
                    elif self.transition_mode == 'pre':
                        self.duration = self.position - remain
                        raise StopIteration()

                    self._exit = True
                    result = (next_duration, next_midi)

                note = Note(duration=result[0], event=Chord(result[1]))
                if self._first == True:
                    if self.name != None:
                        try:
                            print
                            'time_line.field.adding lyric name'
                            note.add_lyric(Lyric(str(self.name)))
                        except Exception as err:
                            print
                            err
                    self._first = False
                # note.add_lyric(Lyric(str(self.name)))
                self._simple_format.add_note(note)
                return note
            else:
                try:
                    next_note = deepcopy(self.note_producer.next())
                except Exception as err:
                    print
                    'time_line: note_producer: err: ', err
                    next_note = deepcopy(self.note_producer(self.position))
                remain = self.duration - self.position
                self._position += next_note.duration
                if self._position < self.duration:
                    pass
                    # result=next_note

                elif self._position == self.duration:
                    self._exit = True
                    # result=next_note

                elif self._position > self.duration:
                    if self.transition_mode == None:
                        next_note.duration = remain
                        self._position = self.duration
                    elif self.transition_mode == 'post':
                        self.duration = self.position
                    elif self.transition_mode == 'pre':
                        self.duration = self.position - remain
                        raise StopIteration()

                    self._exit = True
                    # result=(next_duration, next_midi)

                if self._first == True:
                    if self.name != None:
                        try:
                            next_note.add_lyric(Lyric(str(self.name)))
                        except Exception as err:
                            print
                            err
                    self._first = False
                # note.add_lyric(Lyric(str(self.name)))
                self._simple_format.add_note(next_note)
                return next_note



        except StopIteration:
            raise StopIteration()

    @property
    def simple_format(self):
        list(self)
        return self._simple_format


class TimeLine(object):
    def __init__(self, *fields):
        self._fields = []
        self.fields = fields
        self._current_field = None
        self._field_iter = None
        self._simple_format = None

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, values):
        self._fields = []
        for value in values:
            if hasattr(value, '__iter__'):
                for v in value:
                    self.add_field(v)
            else:
                self.add_field(value)

    def add_field(self, field):
        # print 'TimeLine is adding field', field
        if field == None:
            field = Field()
        if not isinstance(field, Field):
            raise TypeError('wrong type for Field')
        else:
            self._fields.append(field)

    def __iter__(self):
        return self

    def next(self):
        if self._simple_format == None:
            self._simple_format = SimpleFormat()
        if self._current_field == None:
            self._field_iter = iter(self.fields)
            self._current_field = self._field_iter.next()
        try:
            note = self._current_field.next()
            self._simple_format.add_note(note)
            return note
        except:
            try:
                self._current_field = self._field_iter.next()
                self.next()
            except:
                raise StopIteration()

    @property
    def simple_format(self):
        print
        'getting simple_format Time Line'
        if self._simple_format == None:
            list(self)
        return self._simple_format

    # class Breathe(TimeLine):


#     def __init__(self, durations=None, inspiration=None, climax=None, expiration=None, repose=None):
#         super(Breathe, self).__init__(None, None, None, None)
#         self._durations=[None, None, None, None]
#         self.durations=durations
#         self._inspiration=None
#         self.inspiration=inspiration
#         self._climax=None
#         self.climax=climax
#         self._expiration=None
#         self.expiration=expiration
#         self.repose=None
#         self.repose=repose
#
#
#
#     @property
#     def inspiration(self):
#         return self.fields[0]
#     @inspiration.setter
#     def inspiration(self, value):
#         if value!=None and not isinstance(value, Field):
#             raise TypeError('inspiration value should be of type Field. If None a new instance of Field() will be assigned')
#         elif value==None:
#             field=Field()
#             field.duration=self.durations[0]
#             self.fields[0]=field
#         else:
#             field=value
#             if self.durations[0]!=None:
#                 field.duration=self.durations[0]
#
#         self.fields[0]=field
#
#     @property
#     def climax(self):
#         return self.fields[1]
#     @climax.setter
#     def climax(self, value):
#         if value!=None and not isinstance(value, Field):
#             raise TypeError('climax value should be of type Field. If None a new instance of Field() will be assigned')
#         elif value==None:
#             field=Field()
#             field.duration=self.durations[1]
#             self.fields[1]=field
#         else:
#             field=value
#             if self.durations[1]!=None:
#                 field.duration=self.durations[1]
#
#         self.fields[1]=field
#
#
#     @property
#     def expiration(self):
#         return self.fields[2]
#     @expiration.setter
#     def expiration(self, value):
#         if value!=None and not isinstance(value, Field):
#             raise TypeError('expiration value should be of type Field. If None a new instance of Field() will be assigned')
#         elif value==None:
#             field=Field()
#             field.duration=self.durations[2]
#             self.fields[2]=field
#         else:
#             field=value
#             if self.durations[2]!=None:
#                 field.duration=self.durations[2]
#
#         self.fields[2]=field
#
#     @property
#     def repose(self):
#         return self.fields[3]
#     @repose.setter
#     def repose(self, value):
#         if value!=None and not isinstance(value, Field):
#             raise TypeError('repose value should be of type Field. If None a new instance of Field() will be assigned')
#         elif value==None:
#
#             field=Field()
#             field.duration=self.durations[3]
#             self.fields[3]=field
#         else:
#             field=value
#             if self.durations[3]!=None:
#                 field.duration=self.durations[3]
#
#         self.fields[3]=field
#
#
#
#     @TimeLine.fields.getter
#     def fields(self):
#         self._fields[0].name='inspiration'
#         self._fields[1].name='climax'
#         self._fields[2].name='expiration'
#         self._fields[3].name='repose'
#         return self._fields
#
#
#     @property
#     def durations(self):
#         return [self.inspiration.duration, self.climax.duration, self.expiration.duration, self.repose.duration]
#     @durations.setter
#     def durations(self, value):
#         try:
#             self.inspiration.duration=value[0]
#             try:
#                 self.climax.duration=value[1]
#                 try:
#                     self.expiration.duration=value[2]
#                     try:
#                         self.repose.duration=value[3]
#                     except:
#                         pass
#                 except:
#                     pass
#             except:
#                 pass
#         except Exception as err:
#             pass
#
#
#     def add_field(self, field):
#         if len(self._fields)<4:
#             if field==None:
#                 field=Field()
#             if not isinstance(field, Field):
#                 raise TypeError('wrong type for Field')
#             else:
#                 self._fields.append(field)
#         else:
#             raise Exception('Breath() does not support add_field')


class Breathe(TimeLine):
    def __init__(self, duration=None, proportions=None, durations=None, repose_1=None, inspiration=None, climax=None,
                 expiration=None, repose_2=None):
        super(Breathe, self).__init__(None, None, None, None, None)
        self._duration = None
        self._proportions = None
        self._durations = [None, None, None, None, None]

        self.duration = duration
        self.proportions = proportions
        self.durations = durations

        self._repose_1 = None
        self.repose_1 = repose_1
        self._inspiration = None
        self.inspiration = inspiration
        self._climax = None
        self.climax = climax
        self._expiration = None
        self.expiration = expiration
        self.repose_2 = None
        self.repose_2 = repose_2

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value
        self.calculate_durations()

    @property
    def repose_1(self):
        return self.fields[0]

    @repose_1.setter
    def repose_1(self, value):
        if value != None and not isinstance(value, Field):
            raise TypeError(
                'repose_1 value should be of type Field. If None a new instance of Field() will be assigned')
        elif value == None:

            field = Field()
            field.duration = self.durations[0]
            self.fields[0] = field
        else:
            field = value
            if self.durations[0] != None:
                field.duration = self.durations[0]

        self.fields[0] = field

    @property
    def inspiration(self):
        return self.fields[1]

    @inspiration.setter
    def inspiration(self, value):
        if value != None and not isinstance(value, Field):
            raise TypeError(
                'inspiration value should be of type Field. If None a new instance of Field() will be assigned')
        elif value == None:
            field = Field()
            field.duration = self.durations[1]
            self.fields[1] = field
        else:
            field = value
            if self.durations[1] != None:
                field.duration = self.durations[1]

        self.fields[1] = field

    @property
    def climax(self):
        return self.fields[2]

    @climax.setter
    def climax(self, value):
        if value != None and not isinstance(value, Field):
            raise TypeError('climax value should be of type Field. If None a new instance of Field() will be assigned')
        elif value == None:
            field = Field()
            field.duration = self.durations[2]
            self.fields[2] = field
        else:
            field = value
            if self.durations[2] != None:
                field.duration = self.durations[2]

        self.fields[2] = field

    @property
    def expiration(self):
        return self.fields[3]

    @expiration.setter
    def expiration(self, value):
        if value != None and not isinstance(value, Field):
            raise TypeError(
                'expiration value should be of type Field. If None a new instance of Field() will be assigned')
        elif value == None:
            field = Field()
            field.duration = self.durations[3]
            self.fields[3] = field
        else:
            field = value
            if self.durations[3] != None:
                field.duration = self.durations[3]

        self.fields[3] = field

    @property
    def repose_2(self):
        return self.fields[4]

    @repose_2.setter
    def repose_2(self, value):
        if value != None and not isinstance(value, Field):
            raise TypeError(
                'repose_2 value should be of type Field. If None a new instance of Field() will be assigned')
        elif value == None:

            field = Field()
            field.duration = self.durations[4]
            self.fields[4] = field
        else:
            field = value
            if self.durations[4] != None:
                field.duration = self.durations[4]

        self.fields[4] = field

    @TimeLine.fields.getter
    def fields(self):
        self._fields[0].name = 'repose_1'
        self._fields[1].name = 'inspiration'
        self._fields[2].name = 'climax'
        self._fields[3].name = 'expiration'
        self._fields[4].name = 'repose_2'
        return self._fields

    def calculate_durations(self):
        if self.duration != None and self.proportions != None:
            self.durations = [proportion * float(self.duration) / sum(self.proportions) for proportion in
                              self.proportions]

    @property
    def proportions(self):
        return self._proportions

    @proportions.setter
    def proportions(self, values):
        self._proportions = values
        self.calculate_durations()

    @property
    def durations(self):
        return [self.repose_1.duration, self.inspiration.duration, self.climax.duration, self.expiration.duration,
                self.repose_2.duration]

    @durations.setter
    def durations(self, values):
        try:
            self.repose_1.duration = values[0]
            try:
                self.inspiration.duration = values[1]
                try:
                    self.climax.duration = values[2]
                    try:
                        self.expiration.duration = values[3]
                        try:
                            self.repose_2.duration = values[4]
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
            except:
                pass
        except Exception as err:
            pass

    def add_field(self, field):
        if len(self._fields) < 5:
            if field == None:
                field = Field()
            if not isinstance(field, Field):
                raise TypeError('wrong type for Field')
            else:
                self._fields.append(field)
        else:
            raise Exception('Breath() does not support add_field')
