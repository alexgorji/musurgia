import os

from prettytable import PrettyTable
from quicktions import Fraction

from musurgia.fractaltree.fractalmusic import FractalMusic
from musurgia.fractaltree.fractaltree import FractalTreeException


class Module(FractalMusic):
    def __init__(self, row_number=None, column_number=None, *args, **kargs):
        super().__init__(*args, **kargs)
        self.row_number = row_number
        self.column_number = column_number
        self._parent_row = None
        self._parent_square = None
        self._parent_column = None
        self._name = None

    @property
    def parent_square(self):
        return self._parent_square

    @property
    def parent_row(self):
        return self._parent_row

    @property
    def parent_column(self):
        return self._parent_column

    def change_duration(self, new_duration):
        if self.parent_square:
            self.parent_square.change_module_duration(self.row_number, self.column_number, new_duration)
        else:
            raise ValueError('parent_square is not set')

    def change_quarter_duration(self, new_quarter_duration):
        if self.parent_square:
            self.parent_square.change_module_quarter_duration(self.row_number, self.column_number, new_quarter_duration)
        else:
            raise ValueError('parent_square is not set')

    def set_name(self, value):
        self._name = value

    @property
    def __name__(self):
        if self._name:
            return self._name

        if self.row_number and self.column_number:
            return str(self.row_number) + '_' + str(self.column_number)
        else:
            return super().__name__

    def write_square_infos(self, text_path, show_quarter_durations=False):
        os.system('touch ' + text_path)
        file = open(text_path, 'w')
        file.write("module_tempo: " + str(self.module_tempo))
        file.write("\n")
        file.write("score_tempo: " + str(self.score_tempo))
        file.write("\n")
        x = PrettyTable(hrules=1)

        leaf_names = [leaf.__name__ for leaf in self.traverse_leaves()]
        leaf_fractal_orders = [leaf.fractal_order for leaf in self.traverse_leaves()]

        leaf_durations = [leaf.duration * self.module_tempo / self.score_tempo for leaf in
                          self.traverse_leaves()]

        rounded_leaf_durations = [round(float(dur), 2) for dur in leaf_durations]

        leaf_quarter_durations = [leaf.quarter_duration for leaf in self.traverse_leaves()]
        rounded_quarter_durations = [round(float(dur), 2) for dur in leaf_quarter_durations]

        x.field_names = ["name", "info", *leaf_names, "sum"]
        x.add_row([self.__name__, 'frac_ord', *leaf_fractal_orders, " "])
        x.add_row([self.__name__, 'durations', *rounded_leaf_durations, round(float(sum(leaf_durations)), 2)])
        x.add_row(
            [self.__name__, 'quarter_dur', *rounded_quarter_durations, round(float(sum(leaf_quarter_durations)), 2)])

        file.write(x.get_string())
        file.close()

    # def get_time_line(self, factor=1, **kwargs):
    #     return TreeTimeLine(length=self.quarter_duration, factor=factor, **kwargs)

    # def get_pdf(self, factor=None):
    #     pdf = Pdf(orientation='landscape')
    #
    #     # pdf.set_margins(20, 20, 20)
    #
    #     pdf.write_line(txt=self.__name__)
    #     pdf.write_line(txt='tree_permutation_order: ' + str(self.tree_permutation_order))
    #     pdf.write_line(txt='permutation_order: ' + str(self.permutation_order))
    #
    #     pdf.write_line(txt='module_tempo: ' + str(self.module_tempo))
    #     pdf.write_line(txt='score_tempo: ' + str(self.score_tempo))
    #     pdf.write_line(txt='quarter_duration: ' + str(self.quarter_duration))
    #     pdf.write_line(txt='duration: ' + str(round(float(self.actual_duration), 2)))
    #
    #     if factor is None:
    #         factor = (pdf.w - pdf.l_margin - pdf.r_margin) / self.quarter_duration
    #
    #     module_tl = TreeTimeLine(length=self.quarter_duration, factor=factor)
    #     label_6 = Label(text=round(float(self.quarter_duration), 2), relative_y=-1,
    #                     relative_x=self.quarter_duration * module_tl.factor / 2)
    #     label_6.font.size = 5
    #     module_tl.mark_line.add_label(label_6)
    #
    #     label_7 = Label(text=round(float(self.actual_duration), 2), relative_y=1,
    #                     relative_x=self.quarter_duration * module_tl.factor / 2)
    #     label_7.font.size = 5
    #     module_tl.mark_line.add_label(label_7)
    #
    #     for child in self.get_children():
    #         child_tl = module_tl.add_child(TreeTimeLine(length=child.quarter_duration, x_offset=None, y_offset=None))
    #
    #         label_1 = Label(text=child.fractal_order)
    #         label_1.font.size = 5
    #         child_tl.mark_line.add_label(label_1)
    #
    #         label_2 = Label(text=round(float(child.quarter_position_in_tree), 2), relative_y=5)
    #         label_2.font.size = 5
    #         child_tl.mark_line.add_label(label_2)
    #
    #         label_3 = Label(text=round(float(child.position_in_score), 2), relative_y=7)
    #         label_3.font.size = 5
    #         child_tl.mark_line.add_label(label_3)
    #
    #         label_4 = Label(text=round(float(child.quarter_duration), 2), relative_y=-1,
    #                         relative_x=child.quarter_duration * child_tl.factor / 2)
    #         label_4.font.size = 5
    #         child_tl.mark_line.add_label(label_4)
    #
    #         label_5 = Label(text=round(float(child.actual_duration), 2), relative_y=1,
    #                         relative_x=child.quarter_duration * child_tl.factor / 2)
    #         label_5.font.size = 5
    #         child_tl.mark_line.add_label(label_5)
    #
    #     pdf.add_time_line(module_tl)
    #
    #     return pdf

    def __deepcopy__(self, memodict={}):
        copied = super().__deepcopy__(memodict)
        copied.row_number = self.row_number
        copied.column_number = self.column_number

        return copied


class RowColumn(object):
    def __init__(self, square, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._square = None
        self.square = square
        self._number = None
        self.number = number
        self._modules = []

    @property
    def square(self):
        return self._square

    @square.setter
    def square(self, value):
        if not isinstance(value, Square):
            raise TypeError('square.value must be of type Square not {}'.format(type(value)))
        self._square = value

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        if not isinstance(value, int):
            raise TypeError('number.value must be of type int not {}'.format(type(value)))
        if not 0 < value <= self.square.side_size:
            raise ValueError('number.value must be of between 0 and {}'.format(self.square.side_size))
        self._number = value

    @property
    def modules(self):
        return self._modules

    def get_module(self, number):
        return self.modules[number - 1]

    @property
    def duration(self):
        return sum([module.quarter_duration for module in self.modules])


class Row(RowColumn):
    def __init__(self, square, number, *args, **kwargs):
        super().__init__(square, number, *args, **kwargs)
        self._name = None

    def _add_module(self, module):
        module._parent_row = self
        self._modules.append(module)

    def set_module_tempo(self, tempo):
        for module in self.modules:
            module.module_tempo = tempo

    def set_score_tempo(self, tempo):
        for module in self.modules:
            module.score_tempo = tempo

    def set_name(self, val):
        self._name = val

    @property
    def __name__(self):
        return self._name


class Column(RowColumn):
    def __init__(self, square, number, *args, **kwargs):
        super().__init__(square, number, *args, **kwargs)

    def _add_module(self, module):
        module._parent_column = self
        self._modules.append(module)


class Square(object):
    def __init__(self, duration, proportions, tree_permutation_order, first_multi=(1, 1),
                 reading_direction='horizontal'):

        self._duration = None
        self._proportions = None
        self._modules = {}
        self._tree_permutation_order = None
        self._first_multi = (1, 1)
        self._reading_direction = None
        self._side_size = None

        self.duration = duration
        self.proportions = proportions
        self.reading_direction = reading_direction
        self.tree_permutation_order = tree_permutation_order
        self.first_multi = first_multi
        self._rows = None
        self._columns = None

    @property
    def side_size(self):
        return self._side_size

    @property
    def duration(self):
        if self.modules != {}:
            durations = map(lambda module: module.duration, self.modules.values())
            self._duration = sum(durations)
        return self._duration

    @duration.setter
    def duration(self, value):
        if value is None:
            raise ValueError('duration cannot be None')
        self._duration = value
        self._calculate_module_values()

    @property
    def proportions(self):
        return self._proportions

    @proportions.setter
    def proportions(self, values):
        if values is None:
            raise ValueError('proportions cannot be None')
        if self.side_size is not None:
            if len(values) != self.side_size:
                raise ValueError('wrong proportions length')
        else:
            self._side_size = len(values)
        self._proportions = values
        self._calculate_module_values()

    @property
    def tree_permutation_order(self):
        return self._tree_permutation_order

    @tree_permutation_order.setter
    def tree_permutation_order(self, values):
        if values is None:
            raise ValueError('tree_permutation_order cannot be None')
        if self.side_size is not None:
            if len(values) != self.side_size:
                raise ValueError('wrong tree_permutation_order length')
        else:
            self._side_size = len(values)
        self._tree_permutation_order = values
        self._calculate_module_values()

    @property
    def modules(self):
        return self._modules

    @property
    def first_multi(self):
        return self._first_multi

    @first_multi.setter
    def first_multi(self, value):
        self._first_multi = value
        if self._modules != {}:
            for key in self._modules.keys():
                module = self._modules[key]
                module.multi = self.index_to_r_c(
                    self.r_c_to_index(module.row_number, module.column_number) + self.r_c_to_index(self.first_multi[0],
                                                                                                   self.first_multi[1]))

    @property
    def reading_direction(self):
        return self._reading_direction

    @reading_direction.setter
    def reading_direction(self, val):
        if self._reading_direction:
            raise FractalTreeException('reading_direction can only be set during initialisation')
        permitted = ['horizontal', 'vertical']
        if val not in permitted:
            raise ValueError('reading_direction.value {} must be in {}'.format(val, permitted))
        self._reading_direction = val

    def get_module(self, *args):
        args = tuple(args)
        return self.modules[args]

    def get_all_modules(self):
        return self.modules.values()

    @property
    def rows(self):
        if self._rows is None:
            self._rows = []
            for row_number in range(1, self.side_size + 1):
                row = Row(square=self, number=row_number)
                for column_number in range(1, self.side_size + 1):
                    module = self.get_module(row_number, column_number)
                    row._add_module(module)

                self._rows.append(row)
        return self._rows

    @property
    def columns(self):
        if self._columns is None:
            self._columns = []
            for column_number in range(1, self.side_size + 1):
                column = Column(square=self, number=column_number)
                for row_number in range(1, self.side_size + 1):
                    module = self.get_module(row_number, column_number)
                    column._add_module(module)

                self._columns.append(column)
        return self._columns

    def get_row(self, row_number):
        return self.rows[row_number - 1]

    def get_column(self, column_number):
        return self.columns[column_number - 1]

    def index_to_r_c(self, index):
        row = int(index / self.side_size) % self.side_size + 1
        column = index % self.side_size + 1
        return row, column

    def r_c_to_index(self, row, column):
        index = ((row - 1) * self.side_size) + (column - 1)
        return index

    def _calculate_module_values(self):
        if self.duration is not None and self.proportions is not None and self.tree_permutation_order is not None:
            row_durations = [self.duration * prop / float(sum(self.proportions)) for prop in self.proportions]
            for (row, column) in [(i + 1, j + 1) for i in range(self.side_size) for j in range(self.side_size)]:
                module_durations = [row_durations[row - 1] * prop / float(sum(self.proportions)) for prop in
                                    self.proportions]
                multi = self.index_to_r_c(
                    self.r_c_to_index(row, column) + self.r_c_to_index(self.first_multi[0], self.first_multi[1]))
                module = Module(duration=module_durations[column - 1],
                                tree_permutation_order=self.tree_permutation_order, proportions=self.proportions,
                                multi=multi, reading_direction=self.reading_direction)
                (module.row_number, module.column_number) = (row, column)
                self._modules[(row, column)] = module
                module._parent_square = self

    def change_module_quarter_duration(self, row_number, column_number, new_quarter_duration):
        factor = Fraction(Fraction(new_quarter_duration),
                          Fraction(self.get_module(row_number, column_number).quarter_duration))

        for key in self.modules:
            self.modules[key].duration = self.modules[key].duration * factor

    def change_module_duration(self, row_number, column_number, new_duration, mode='module_duration'):
        if mode == 'module_duration':
            factor = Fraction(Fraction(new_duration), Fraction(self.get_module(row_number, column_number).duration))
        elif mode == 'score_duration':
            factor = Fraction(Fraction(new_duration),
                              Fraction(self.get_module(row_number, column_number).score_duration))
        else:
            raise ValueError()

        for key in self.modules:
            self.modules[key].duration = self.modules[key].duration * factor

    def round_quarter_durations(self):
        for module in self.modules.values():
            module.quarter_duration = round(module.quarter_duration)

    def write_infos(self, text_path, show_row_name=False, show_score_tempo=False, show_module_tempo=False,
                    show_quarter_durations=False):
        os.system('touch ' + text_path)
        file = open(text_path, 'w')
        x = PrettyTable(hrules=1)

        column_numbers = [str(number) for number in range(1, self.side_size + 1)]
        if show_row_name:
            x.field_names = ["row", 'row_name', "column:", *column_numbers]
        else:
            x.field_names = ["row", "column:", *column_numbers]

        for row_number in range(1, self.side_size + 1):
            row = self.get_row(row_number)
            if show_row_name:
                row_info = [row_number, row.__name__]
            else:
                row_info = [row_number]

            module_tempi = [module.module_tempo for module in row.modules]
            score_tempi = [module.score_tempo for module in row.modules]
            score_durations = [module.rounded_score_duration for module in row.modules]

            quarter_durations = [round(float(module.quarter_duration), 2) for module in row.modules]

            if show_module_tempo:
                x.add_row([*row_info, 'mod_tempo', *module_tempi])

            if show_score_tempo:
                x.add_row([*row_info, 'sc_tempo', *score_tempi])

            if show_quarter_durations:
                x.add_row([*row_info, 'quarter_dur', *quarter_durations])

            x.add_row([*row_info, 'duration', *score_durations])

        file.write(x.get_string())
        file.close()

# class Selection(object):
#
#     def __init__(self, *modules, **kwargs):
#         super().__init__(**kwargs)
#         self._modules = None
#         self._time_lines = {}
#         self.modules = modules
#
#     @property
#     def time_lines(self):
#         return self._time_lines
#
#     @property
#     def modules(self):
#         return self._modules
#
#     @modules.setter
#     def modules(self, val):
#         self.remove_modules()
#         for v in val:
#             self.add_module(v)
#
#     def remove_modules(self):
#         self._modules = []
#
#     def _get_last_position_in_time_lines(self):
#         positions = [v.x_offset + v.length for v in self._time_lines.values()]
#         try:
#             return max(positions)
#         except ValueError:
#             return 0
#
#     def add_module(self, module):
#         if not isinstance(module, Module):
#             raise TypeError('added module must be of type not{}'.format(type(module)))
#         self._modules.append(module)
#         x_offset = self._get_last_position_in_time_lines()
#         self._time_lines[module] = module.get_time_line(x_offset=x_offset)

# def get_pdf(self):
#     pdf = Pdf(orientation='landscape')
#     for time_line in self.time_lines.values():
#         pdf.add_time_line(time_line)
#
#     return pdf
