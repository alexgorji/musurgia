from musurgia.musurgia_types import check_type, PositionType
from musurgia.pdf.drawobject import HasGetHeightProtocol
from musurgia.pdf.positioned import SlavePositionGetter, HasPositionsProtocol
from musurgia.pdf.text import TextLabel


class Labeled(SlavePositionGetter, HasPositionsProtocol, HasGetHeightProtocol):
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

        return label

    def add_label(self, label, **kwargs):
        return self.add_text_label(label, **kwargs)

    def get_above_text_labels(self):
        return self._above_text_labels

    def get_below_text_labels(self):
        return self._below_text_labels

    def get_left_text_labels(self):
        return self._left_text_labels

    def get_text_labels(self):
        return self.get_left_text_labels() + self.get_above_text_labels() + self.get_below_text_labels()

    def draw_above_text_labels(self, pdf):
        if self.get_above_text_labels():
            with pdf.saved_state():
                translate_y = -self.get_above_text_labels_height() + self.get_above_text_labels()[-1].get_text_height()
                pdf.translate(0, translate_y)
                for text_label in self.get_above_text_labels():
                    text_label.draw(pdf)
                    pdf.translate(0, text_label.get_height())

    def draw_below_text_labels(self, pdf):
        if self.get_below_text_labels():
            with pdf.saved_state():
                pdf.translate(self.relative_x, self.get_height())
                for text_label in self.get_below_text_labels():
                    pdf.translate(0, text_label.get_height())
                    text_label.draw(pdf)

    def draw_left_text_labels(self, pdf):
        if self.get_left_text_labels():
            with pdf.saved_state():
                pdf.translate(0, -self.get_left_text_labels_height() / 2)
                for text_label in self.get_left_text_labels():
                    pdf.translate(0, text_label.get_height())
                    with pdf.saved_state():
                        pdf.translate(-(text_label.get_width()), 0)
                        text_label.draw(pdf)

    def get_slave_position(self, slave, position: PositionType):
        check_type(position, 'PositionType', class_name=self.__class__.__name__, method_name='get_slave_position',
                   argument_name='position')
        if position == 'x':
            return 0
        elif position == 'y':
            if slave.placement in ['l', 'left']:
                return self.get_height() / 2
            return 0

    def get_above_text_labels_height(self):
        return sum([tl.get_height() for tl in self.get_above_text_labels()])

    def get_left_text_labels_height(self):
        return sum([tl.get_height() for tl in self.get_left_text_labels()])
