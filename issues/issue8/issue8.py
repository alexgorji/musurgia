import os
from fractions import Fraction
from itertools import cycle

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.chordfield.chordfield import Breathe, ChordField
from musurgia.chordfield.valuegenerator import ValueGenerator

path = str(os.path.abspath(__file__).split('.')[0])
score = TreeScoreTimewise()
proportions = (1, 10, 1, 7, 1)
breakpoints = (1, Fraction(1, 7), 1)
quarter_durations = [8, 12]
breathe = Breathe(proportions=proportions, breakpoints=breakpoints, quarter_duration=sum(quarter_durations),
                  quantize=1)
###
breathe = breathe.__deepcopy__()
breathe.midi_generator = ValueGenerator(cycle([60]))
###
parent_chord_field = ChordField(duration_generator=breathe.duration_generator.__deepcopy__())
for i in range(len(quarter_durations)):
    quarter_duration = quarter_durations[i]
    midi = 60 + i
    parent_chord_field.add_child(
        ChordField(midi_generator=ValueGenerator(cycle([midi])), long_ending_mode='self_extend',
                   short_ending_mode='self_shrink', quarter_duration=quarter_duration))
####
copy_parent_chord_field = parent_chord_field.__deepcopy__()


####
# print([child.quarter_duration for child in copy_parent_chord_field.children])
# def get_positions(chord_field):
#     for child in chord_field.children:
#         while True:
#             try:
#                 print('position: {}, position_in_parent: {}'.format(float(child.position), float(child.position_in_parent)))
#
#                 print('next_child.quarter_duration: {}'.format(float(child.__next__().quarter_duration)))
#             except StopIteration:
#                 break
#
#
# get_positions(parent_chord_field)
####
breathe.simple_format.to_stream_voice().add_to_score(score=score, part_number=1)
parent_chord_field.simple_format.to_stream_voice().add_to_score(score=score, part_number=2)
simple_format = SimpleFormat()
for child in copy_parent_chord_field.children:
    simple_format.extend(child.simple_format)
simple_format.to_stream_voice().add_to_score(score=score, part_number=3)
###

xml_path = path + '_test_1.xml'
score.write(xml_path)
