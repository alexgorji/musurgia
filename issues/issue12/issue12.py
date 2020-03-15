import os

from musicscore.musictree.treescoretimewise import TreeScoreTimewise

from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])

fm = FractalMusic(tree_permutation_order=(2, 6, 4, 1, 3, 7, 5), tempo=56, duration=45 / 2, multi=(2, 6))
fm.generate_children(number_of_children=4)
score = TreeScoreTimewise()
fm.get_simple_format(layer=fm.number_of_layers).to_stream_voice().add_to_score(score)

xml_path = path + '.xml'
score.write(xml_path)
