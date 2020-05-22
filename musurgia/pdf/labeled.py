from musurgia.pdf.masterslave import PositionMaster
from musurgia.pdf.text import TextLabel


class Labeled(PositionMaster):
    def __init__(self, distance_between_labels=3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._above_text_labels = []
        self._below_text_labels = []
        self.distance_between_labels = distance_between_labels

    def add_text_label(self, label, **kwargs):
        if not isinstance(label, TextLabel):
            label = TextLabel(label, **kwargs)
        label.master = self
        if label.placement == 'above':
            self._above_text_labels.append(label)
        else:
            self._below_text_labels.append(label)

        return label

    def add_label(self, label, **kwargs):
        return self.add_text_label(label, **kwargs)

    @property
    def above_text_labels(self):
        return self._above_text_labels

    @property
    def below_text_labels(self):
        return self._below_text_labels

    @property
    def text_labels(self):
        return self.above_text_labels + self.below_text_labels

    def draw_above_text_labels(self, pdf):
        for text_label in self.above_text_labels:
            text_label.draw(pdf)
            pdf.translate(0, text_label.get_text_height())

    def draw_below_text_labels(self, pdf):
        for text_label in self.below_text_labels:
            text_label.draw(pdf)
            pdf.translate(0, text_label.get_text_height())

    def get_slave_position(self, slave, position):
        if position == 'x':
            return self.relative_x
        elif position == 'y':
            return 0
        else:
            raise AttributeError(position)

    def get_above_labels_height(self):
        if self.above_text_labels:
            return sum([l.get_height() for l in self.above_text_labels])
        return 0

    def get_below_labels_height(self):
        if self.below_text_labels:
            return sum([l.get_height() for l in self.above_text_labels])
        return 0
