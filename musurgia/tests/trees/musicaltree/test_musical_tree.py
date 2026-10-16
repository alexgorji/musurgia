from pathlib import Path
from itertools import cycle
from typing import assert_type
from unittest import TestCase

from musurgia.tests.helpers import (
    XMLTestCase,
    test_fractal_structure_list,
)

from musurgia.trees.musicaltree import (
    FractalDirectionIterator,
    FractalMusicalTree,
    FractalRelativeMusicTree,
    FractalRelativeTreeChordFactory,
    MagicRandomTreeMidiGenerator,
    MusicalTree,
    RelativeMusicTree,
    RelativeTreeChordFactory,
    TreeChordFactory,
)
from musurgia.trees.timelinetree import TimelineDuration

path = Path(__file__)


class TestTreeFactoryContracts(TestCase):
    def test_factory_return_types(self) -> None:
        tree = MusicalTree(duration=TimelineDuration(10))
        relative = RelativeMusicTree(duration=TimelineDuration(10))
        fractal = FractalMusicalTree(duration=TimelineDuration(10), proportions=(1, 2))
        fractal_relative = FractalRelativeMusicTree(
            duration=TimelineDuration(10), proportions=(1, 2)
        )
        assert_type(tree.get_chord_factory(), TreeChordFactory)
        assert_type(relative.get_chord_factory(), RelativeTreeChordFactory)
        assert_type(fractal.get_chord_factory(), TreeChordFactory)
        assert_type(
            fractal_relative.get_chord_factory(), FractalRelativeTreeChordFactory
        )
        assert_type(
            fractal_relative.get_chord_factory().direction_iterator,
            FractalDirectionIterator,
        )
        relative.get_chord_factory().midi_value_range = (60, 84)
        fractal_relative.get_chord_factory().direction_iterator.main_direction_cell = [
            1,
            1,
        ]

    def test_factory_replacement(self) -> None:
        class CustomFactory(FractalRelativeTreeChordFactory):
            pass

        tree = FractalRelativeMusicTree(
            duration=TimelineDuration(10), proportions=(1, 2)
        )
        tree.set_tree_chord_factory_class(CustomFactory)
        factory = tree.get_chord_factory()
        self.assertIsInstance(factory, CustomFactory)
        for incompatible in (TreeChordFactory, RelativeTreeChordFactory):
            with self.assertRaises(TypeError):
                tree.set_tree_chord_factory_class(incompatible)
            self.assertIs(tree.get_chord_factory(), factory)

        relative = RelativeMusicTree(duration=TimelineDuration(10))
        with self.assertRaises(TypeError):
            relative.set_tree_chord_factory_class(TreeChordFactory)

        plain = MusicalTree(duration=TimelineDuration(10))
        plain.set_tree_chord_factory_class(RelativeTreeChordFactory)
        self.assertIsInstance(plain.get_chord_factory(), RelativeTreeChordFactory)

    def test_fractal_iterator_replacement_and_reset(self) -> None:
        tree = FractalRelativeMusicTree(
            duration=TimelineDuration(10), proportions=(1, 2)
        )
        factory = tree.get_chord_factory()
        iterator = FractalDirectionIterator(
            main_direction_cell=[1, 1], fractal_node=tree
        )
        factory.direction_iterator = iterator
        self.assertIs(factory.direction_iterator, iterator)
        with self.assertRaises(TypeError):
            factory.direction_iterator = cycle([1, -1])
        self.assertIs(factory.direction_iterator, iterator)
        factory.direction_iterator = None
        self.assertIsInstance(factory.direction_iterator, FractalDirectionIterator)
        self.assertEqual(factory.direction_iterator.get_main_directions(), [1, -1])

        relative = RelativeMusicTree(duration=TimelineDuration(10))
        relative.get_chord_factory().direction_iterator = cycle([1, -1])
        directions = relative.get_chord_factory().direction_iterator
        assert directions is not None
        self.assertEqual(next(directions), 1)

    def test_fractal_factory_copy_on_split(self) -> None:
        tree = FractalRelativeMusicTree(
            duration=TimelineDuration(10), proportions=(1, 2)
        )
        tree.get_chord_factory().midi_value_range = (60, 84)
        for child in tree.split(1, 1):
            assert_type(child, FractalRelativeMusicTree)
            assert_type(child.get_chord_factory(), FractalRelativeTreeChordFactory)
            self.assertEqual(child.get_chord_factory().midi_value_range, (60, 84))
            self.assertIs(child.get_chord_factory().get_musical_tree_node(), child)
            self.assertIsNot(
                child.get_chord_factory().direction_iterator,
                tree.get_chord_factory().direction_iterator,
            )


class TestMusicalTree(XMLTestCase):
    def setUp(self) -> None:
        self.mt = MusicalTree.create_tree_from_list(
            test_fractal_structure_list, ["duration"]
        )
        self.mt.get_chord_factory().show_metronome = True

    def test_musical_tree_root_chord(self) -> None:
        chord = self.mt.get_chord_factory().create_chord()
        self.assertEqual(
            chord.quarter_duration, self.mt.get_duration().get_quarter_duration()
        )
        self.assertEqual(chord.metronome, self.mt.get_duration().get_metronome())


class TestTreeMidiGenerator(XMLTestCase):
    def setUp(self) -> None:
        self.mt = MusicalTree.create_tree_from_list(
            test_fractal_structure_list, ["duration"]
        )
        self.mt.get_chord_factory().show_metronome = True

    def test_random_midis(self) -> None:
        MagicRandomTreeMidiGenerator(
            self.mt, pool=list(range(60, 85)), seed=10, periodicity=7
        ).set_musical_tree_midis()
        score = self.mt.export_score()
        score.get_quantized = True
        with self.file_path(path, "random") as xml_path:
            score.export_xml(xml_path)
