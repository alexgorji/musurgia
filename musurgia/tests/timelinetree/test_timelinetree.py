from unittest import TestCase
from musurgia.musurgia_exceptions import WrongNodeDurationError
from musurgia.timelinetree.timelinetree import TimeLineTree, TimeLineNodeContainer
from musurgia.timing.duration import Duration


class TimeLineTreeTestCase(TestCase):
    def test_create_timeline_tree_root(self):
        tlt = TimeLineTree(Duration(2))
        self.assertTrue(isinstance(tlt.content, TimeLineNodeContainer))
        self.assertEqual(tlt.content.duration.seconds, 2)

    def test_add_child_to_timeline(self):
        root_duration = Duration(2)
        child_durations = [Duration(1.5, 0.5)]
        tlt = TimeLineTree(root_duration)
        [tlt.add_child(TimeLineTree(d)) for d in child_durations ]
        self.assertListEqual([ch.get_duration() for ch in tlt.get_children()], child_durations)

    def test_check_timeline_durations(self):
        tlt = TimeLineTree(Duration(2))
        tlt.add_child(TimeLineTree(Duration(1.5)))
        tlt.add_child(TimeLineTree(Duration(0.5)))
        self.assertTrue(tlt.check_timeline_durations())
        tlt.add_child(TimeLineTree(Duration(1)))
        with self.assertRaises(WrongNodeDurationError) as err:
            tlt.check_timeline_durations()
        self.assertAlmostEqual(str(err.exception), "Children of TimeLineTree node of position 0 with duration 2.0 have wrong durations [1.5, 0.5, 1.0] ")

