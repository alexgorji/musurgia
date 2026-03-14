from unittest import TestCase


from musurgia.graphics.drawobject import Container, Position, TextDrawObject
from musurgia.graphics.mixins import Label, LabeledMixin


class DummyLabeledContainer(LabeledMixin, Container):
    pass


class DummyLabeledNoneContainer(LabeledMixin):
    pass


class LabeledMixinTestCase(TestCase):

    def test_build_labels_error_for_not_container(self):
        with self.assertRaises(TypeError):
            DummyLabeledNoneContainer()

    def test_build_labels(self):
        lc = DummyLabeledContainer(
            labels=[Label("first", offset=Position(10, 20)), Label("second")]
        )

        assert len(lc.get_labels()) == 2
        assert len(lc.get_positioned_draw_objects()) == 2
        positions = {p for p, _ in lc.get_positioned_draw_objects()}
        assert positions == {Position(0, 0), Position(10, 20)}
        for o in lc.get_draw_objects():
            assert isinstance(o, TextDrawObject)
