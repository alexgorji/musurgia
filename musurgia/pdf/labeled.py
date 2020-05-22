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
        return self.left_text_labels + self.above_text_labels + self.below_text_labels + self.right_text_labels

    def draw_above_text_labels(self, pdf):
        with pdf.saved_state():
            for index, text_label in enumerate(self.above_text_labels[::-1]):
                pdf.translate(0, -text_label.get_height())
                text_label.draw(pdf)

    def draw_below_text_labels(self, pdf):
        for text_label in self.below_text_labels:
            pdf.translate(0, text_label.get_text_height())
            text_label.draw(pdf)

    def draw_left_text_labels(self, pdf):
        with pdf.saved_state():
            for index, text_label in enumerate(self.left_text_labels):
                pdf.translate(-(text_label.get_width()+2), text_label.get_height())
                text_label.draw(pdf)
                pdf.translate(text_label.get_width()+2, 0)

    def get_slave_position(self, slave, position):
        if position == 'x':
            # return self.relative_x
            return 0
        elif position == 'y':
            return 0
        else:
            raise AttributeError(position)