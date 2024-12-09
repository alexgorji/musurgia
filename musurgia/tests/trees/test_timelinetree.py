from unittest import TestCase
from musurgia.musurgia_exceptions import WrongNodeDurationError
from musurgia.tests.utils_for_tests import create_test_timeline_tree
from musurgia.trees.timelinetree import TimelineTree, TimeLineNodeContainer
from musurgia.timing.duration import Duration


class TimeLineTreeTestCase(TestCase):
    def test_create_timeline_tree_root(self):
        tlt = TimelineTree(Duration(2))
        self.assertTrue(isinstance(tlt.content, TimeLineNodeContainer))
        self.assertEqual(tlt.content.duration.seconds, 2)

    def test_add_child_to_timeline(self):
        root_duration = Duration(2)
        child_durations = [Duration(1.5, 0.5)]
        tlt = TimelineTree(root_duration)
        [tlt.add_child(TimelineTree(d)) for d in child_durations ]
        self.assertListEqual([ch.get_duration() for ch in tlt.get_children()], child_durations)

    def test_check_timeline_durations(self):
        tlt = TimelineTree(Duration(2))
        tlt.add_child(TimelineTree(Duration(1.5)))
        tlt.add_child(TimelineTree(Duration(0.5)))
        self.assertTrue(tlt.check_timeline_durations())
        tlt.add_child(TimelineTree(Duration(1)))
        with self.assertRaises(WrongNodeDurationError) as err:
            tlt.check_timeline_durations()
        self.assertEqual(str(err.exception), "Children of TimelineTree node of position 0 with duration 2.0 have wrong durations [1.5, 0.5, 1.0] ")

    def test_timeline_get_value(self):
        tft = create_test_timeline_tree()
        expected = """└── 0.0
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
        self.assertEqual(tft.get_tree_representation(key=lambda node: node.get_value()), expected)