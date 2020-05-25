from musurgia.pdf.masterslave import PositionMaster
from musurgia.pdf.text import TextLabel


class Labeled(PositionMaster):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._above_text_labels = []
        self._below_text_labels = []
        self._left_text_labels = []

    def add_text_label(self, label, **kwargs):
        if not isinstance(label, TextLabel):
            label = TextLabel(label, **kwargs)
        label.master = self
        if label.placement == 'above':
            self._above_text_labels.append(label)
        elif label.placement == 'below':
            self._below_text_labels.append(label)
        elif label.placement == 'left':
            self._left_text_labels.append(label)
        else:
            raise AttributeError()

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
    def left_text_labels(self):
        return self._left_text_labels

    @property
    def text_labels(self):
        return self.left_text_labels + self.above_text_labels + self.below_text_labels

    def draw_above_text_labels(self, pdf):
        with pdf.saved_state():
            pdf.translate(0, -self.get_above_text_labels_height())
            for text_label in self.above_text_labels:
                text_label.draw(pdf)
                pdf.translate(0, text_label.get_height())

    def draw_below_text_labels(self, pdf):
        for text_label in self.below_text_labels:
            pdf.translate(0, text_label.get_height())
            text_label.draw(pdf)

    def draw_left_text_labels(self, pdf):
        with pdf.saved_state():
            pdf.translate(0, -self.get_left_text_labels_height() / 2)
            for text_label in self.left_text_labels:
                pdf.translate(0, text_label.get_height())
                with pdf.saved_state():
                    pdf.translate(-(text_label.get_width() + 1), 0)
                    text_label.draw(pdf)

    def get_slave_position(self, slave, position):
        if position == 'x':
            return 0
        elif position == 'y':
            return 0
        else:
            raise AttributeError(position)

    def get_above_text_labels_height(self):
        return sum([tl.get_height() for tl in self.above_text_labels])

    def get_left_text_labels_height(self):
        return sum([tl.get_height() for tl in self.left_text_labels])
