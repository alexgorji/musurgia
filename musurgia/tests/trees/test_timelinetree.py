from unittest import TestCase

from musicscore.metronome import Metronome
from musicscore.quarterduration import QuarterDuration
from musurgia.musurgia_exceptions import WrongTreeValueError
from musurgia.tests.utils_for_tests import create_test_timeline_tree
from musurgia.trees.timelinetree import TimelineDuration, TimelineTree


class TimelineDurationTestCase(TestCase):
    def setUp(self):
        self.tld = TimelineDuration(4)
        return super().setUp()

    def test_set_quarter_duration_error(self):
        with self.assertRaises(AttributeError):
            self.tld.quarter_duration = QuarterDuration(4)

    def test_get_quarter_duration(self):
        self.assertEqual(self.tld.metronome.per_minute, 60)
        self.assertEqual(self.tld.get_quarter_duration(), QuarterDuration(4))

    def test_update_quarter_duration(self):
        self.assertEqual(self.tld.get_quarter_duration(), 4)
        self.tld.metronome = Metronome(120)
        self.assertEqual(self.tld.get_quarter_duration(), 8)
        self.tld._set_seconds(5)
        self.assertEqual(self.tld.get_quarter_duration(), 10)
        self.tld.metronome = Metronome(120, 2)
        self.assertEqual(self.tld.get_quarter_duration(), 20)


class TimeLineTreeTestCase(TestCase):
    def test_create_timeline_tree_root(self):
        tlt = TimelineTree(TimelineDuration(2))
        self.assertEqual(tlt.get_duration().calculate_in_seconds(), 2)

    def test_add_child_to_timeline(self):
        root_duration = TimelineDuration(2)
        child_durations = [TimelineDuration(1.5), TimelineDuration(0.5)]
        tlt = TimelineTree(root_duration)
        [tlt.add_child(TimelineTree(d)) for d in child_durations]
        self.assertListEqual(
            [ch.get_duration() for ch in tlt.get_children()], child_durations
        )

    def test_check_timeline_durations(self):
        tlt = TimelineTree(TimelineDuration(2))
        tlt.add_child(TimelineTree(TimelineDuration(1.5)))
        tlt.add_child(TimelineTree(TimelineDuration(0.5)))
        self.assertTrue(tlt.check_tree_values())
        tlt.add_child(TimelineTree(TimelineDuration(1)))
        with self.assertRaises(WrongTreeValueError) as err:
            tlt.check_tree_values()
        expected = "Children of ValuedTree node of position 0 with value 2 have wrong values [Fraction(3, 2), Fraction(1, 2), Fraction(1, 1)] (sum=3)"
        self.assertEqual(str(err.exception), expected)

    def test_timeline_get_value(self):
        tft = create_test_timeline_tree()
        self.assertEqual(tft.get_value(), 60)
        expected = """└── 60.0
    ├── 20.0
    │   ├── 10.0
    │   ├── 2.0
    │   ├── 3.0
    │   └── 5.0
    ├── 10.0
    └── 30.0
        ├── 5.0
        ├── 20.0
        ├── 3.0
        └── 2.0
"""
        self.assertEqual(
            tft.get_tree_representation(key=lambda node: float(node.get_value())),
            expected,
        )

    def test_timeline_update_duration(self):
        tft = create_test_timeline_tree()
        one_child = tft.get_children()[0].get_children()[0]
        self.assertEqual(one_child.get_value(), 10)
        self.assertEqual(one_child.get_duration(), 10)

        with self.assertRaises(AttributeError):
            one_child.value = 15

        with self.assertRaises(AttributeError):
            one_child.duration.value = 15

        with self.assertRaises(AttributeError):
            one_child.duration.seconds = 15

        with self.assertRaises(AttributeError):
            one_child.duration = TimelineDuration(15)

        one_child.update_duration(15)
        self.assertEqual(one_child.get_value(), 15)
        self.assertEqual(one_child.get_duration(), 15)

        expected = """└── 65.0
    ├── 25.0
    │   ├── 15.0
    │   ├── 2.0
    │   ├── 3.0
    │   └── 5.0
    ├── 10.0
    └── 30.0
        ├── 5.0
        ├── 20.0
        ├── 3.0
        └── 2.0
"""
        self.assertEqual(
            tft.get_tree_representation(key=lambda node: float(node.get_value())),
            expected,
        )
        tft.check_tree_values()

        one_child.update_duration(TimelineDuration(5))
        self.assertEqual(one_child.get_value(), 5)
        self.assertEqual(one_child.get_duration(), 5)
        expected = """└── 55.0
    ├── 15.0
    │   ├── 5.0
    │   ├── 2.0
    │   ├── 3.0
    │   └── 5.0
    ├── 10.0
    └── 30.0
        ├── 5.0
        ├── 20.0
        ├── 3.0
        └── 2.0
"""
        self.assertEqual(
            tft.get_tree_representation(key=lambda node: float(node.get_value())),
            expected,
        )

        tft.check_tree_values()
