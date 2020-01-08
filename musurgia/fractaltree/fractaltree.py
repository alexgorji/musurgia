import itertools

from quicktions import Fraction

from musurgia.permutation import LimitedPermutation, permute
from musurgia.tree import Tree


class FractalTreeException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, kwargs)


class FractalTree(Tree):
    def __init__(self, proportions=None, tree_permutation_order=None, value=None, multi=None, fertile=True,
                 reading_direction='horizontal', *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self._value = None
        self._proportions = None
        self._tree_permutation_order = None
        self._multi = None
        self._permutation_order = None
        self._fertile = None
        self._reading_direction = None
        self._fractal_order = None
        self._children_fractal_values = None
        self._name = None

        self.proportions = proportions
        self.tree_permutation_order = tree_permutation_order
        self.value = value
        self.multi = multi
        self.fertile = fertile
        self.reading_direction = reading_direction

    @property
    def proportions(self):
        return self._proportions

    @proportions.setter
    def proportions(self, values):
        if values is None:
            values = [1, 2, 3]
        self._proportions = [Fraction(Fraction(value) / Fraction(sum(values))) for value in values]

    @property
    def tree_permutation_order(self):
        return self._tree_permutation_order

    @tree_permutation_order.setter
    def tree_permutation_order(self, values):
        if values is None:
            values = [3, 1, 2]
        self._tree_permutation_order = values
        self._permutation_order = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if val is None:
            self._value = 10
        else:
            self._value = val
        if self._value == 0:
            self.fertile = False

    @property
    def multi(self):
        return self._multi

    @multi.setter
    def multi(self, vals):
        if vals is None:
            vals = (1, 1)

        elif not isinstance(vals, tuple) or len(vals) != 2:
            raise TypeError('multi has to be a tuple with a length of 2')
        #
        # m_1 = vals[0]
        # m_2 = vals[1]
        #
        # m_1, m_2 = m_1 % len(self.proportions), m_2 % len(self.proportions)
        # if m_1 == 0:
        #     m_1 = len(self.proportions)
        # if m_2 == 0:
        #     m_2 = len(self.proportions)
        #
        # self._multi = (m_1, m_2)
        self._multi = vals
        self._permutation_order = None

    @property
    def fertile(self):
        return self._fertile

    @fertile.setter
    def fertile(self, val):
        if not isinstance(val, bool):
            raise TypeError('fertile.value must be of type bool not{}'.format(type(val)))
        self._fertile = val

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

    @property
    def permutation_order(self):
        def _calculate_permutation_order():
            if self.tree_permutation_order:
                permutation = LimitedPermutation(input_list=list(range(1, len(self.proportions) + 1)),
                                                 main_permutation_order=self.tree_permutation_order, multi=self.multi,
                                                 reading_direction=self.reading_direction)

                return permutation.permutation_order
            else:
                raise FractalTreeException('tree_permutation_order must be set')

        if self._permutation_order is None:
            self._permutation_order = _calculate_permutation_order()
        return self._permutation_order

    @property
    def fractal_order(self):
        return self._fractal_order

    def calculate_position_in_tree(self):
        parent = self.up
        if self.is_root:
            return 0
        else:
            index = parent.get_children().index(self)
            if index == 0:
                return parent.position_in_tree
            else:
                return parent.get_children()[index - 1].position_in_tree + parent.get_children()[index - 1].value

    @property
    def position_in_tree(self):
        return self.calculate_position_in_tree()

    @property
    def number_of_layers(self):
        if len(self.get_leaves()) == 0:
            return 0
        else:
            return self.get_farthest_leaf().get_distance(self)

    @property
    def __name__(self):
        return self.name

    @__name__.setter
    def __name__(self, val):
        self.name = val

    @property
    def name(self):
        if self._name is None:
            if self.is_root:
                self._name = '0'
            elif self.up.is_root:
                self._name = str(self.up.get_children().index(self) + 1)
            else:
                self._name = self.up.name + '.' + str(self.up.get_children().index(self) + 1)
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def position(self):
        if self.is_root():
            # return self.first_position
            return 0
        else:
            siblings = self.up.children
            index = siblings.index(self)
            previous_siblings = siblings[:index]
            position_in_parent = 0
            for child in previous_siblings: position_in_parent += child.value
            return position_in_parent + self.up.position

    @property
    def children_fractal_values(self):
        if not self._children_fractal_values:
            self._children_fractal_values = self._calculate_children_fractal_values()
        return self._children_fractal_values

    def _calculate_children_fractal_orders(self):
        if self.value and self.proportions:
            children_fractal_orders = range(1, len(self.proportions) + 1)
            permutation_order = self.permutation_order
            if permutation_order:
                children_fractal_orders = permute(children_fractal_orders, permutation_order)
            return children_fractal_orders

    @property
    def children_fractal_orders(self):
        return self._calculate_children_fractal_orders()

    def _calculate_children_fractal_values(self):
        value = self.value
        if value == 0:
            value = 0.01
        if value and self.proportions:
            children_fractal_values = [value * prop for prop in self.proportions]
            if self.permutation_order:
                try:
                    children_fractal_values = permute(children_fractal_values, self.permutation_order)
                except ValueError:
                    raise ValueError('proportions and tree_permutation_order should have the same length')
            return children_fractal_values

    def _child_multi(self, parent, index):
        number_of_children = len(self.proportions)
        multi_first = sum(parent.multi) % number_of_children
        if multi_first == 0:
            multi_first = number_of_children
        ch_multi = (multi_first, index + 1)
        return ch_multi

    def add_self(self):
        leaves = self.get_leaves()
        for leaf in leaves:
            new_node = self.copy()
            new_node._up = self
            new_node._fractal_order = self.fractal_order
            leaf.add_child(new_node)

    def add_layer(self, *conditions):
        leaves = list(self.traverse_leaves())
        if not leaves:
            leaves = [self]

        if conditions:
            for leaf in leaves:
                for condition in conditions:
                    if not condition(leaf):
                        leaf.fertile = False
                        break

        for leaf in leaves:
            if leaf.fertile is True:
                for i in range(len(leaf.proportions)):
                    new_node = leaf.copy()
                    new_node.value = leaf.children_fractal_values[i]
                    new_node.multi = self._child_multi(leaf, i)
                    leaf.add_child(new_node)
                    new_node._fractal_order = leaf.children_fractal_orders[i]

            else:
                pass

    def get_layer(self, layer, key=None):
        if layer <= self.get_root().number_of_layers:
            branch_distances = []
            for child in self.get_children():
                branch_distances.append(child.get_farthest_leaf().get_distance())
            if layer == 0:
                if key:
                    return [getattr(self, key)]
                else:
                    return [self]

            if layer >= 1:
                output = []
                if not branch_distances:
                    output.extend(self.get_layer(layer=layer - 1, key=key))
                for i in range(len(self.get_children())):
                    child = self.get_children()[i]
                    if branch_distances[i] == 1:
                        if key:
                            output.append(getattr(child, key))
                        else:
                            output.append(child)
                    else:
                        if layer == 1:
                            output.extend(child.get_layer(layer - 1, key))
                        else:
                            output.append(child.get_layer(layer - 1, key))

                return output
        else:
            err = 'max layer number=' + str(self.number_of_layers)
            raise ValueError(err)

    @property
    def layers(self):
        return [self.get_layer(i) for i in range(self.number_of_layers + 1)]

    @property
    def next(self):
        if not self.is_leaf():
            raise Exception('FractalTree().next property can only be used for leaves')
        else:
            try:

                parent = self.up
                while parent is not None:
                    parent_leaves = list(parent.traverse_leaves())
                    index = parent_leaves.index(self)
                    try:
                        return parent_leaves[index + 1]
                    except IndexError:
                        parent = parent.up
                raise IndexError()
            except IndexError:
                return None

    def get_previous_leaf(self):
        if not self.is_leaf():
            raise Exception('FractalTree().get_previous_leaf  can only be applied to leaves')
        try:
            parent = self.up
            while parent is not None:
                parent_leaves = list(parent.traverse_leaves())
                index = parent_leaves.index(self)
                try:
                    return parent_leaves[index - 1]
                except IndexError:
                    parent = parent.up
            raise IndexError()
        except IndexError:
            return None

    def get_previous_sibling(self):
        try:
            siblings = self.up.get_children()
            index = siblings.index(self)
            if index == 0:
                return None
            return siblings[index - 1]
        except AttributeError:
            return None

    def get_next_sibling(self):
        try:
            siblings = self.up.get_children()
            index = siblings.index(self)
            return siblings[index + 1]
        except (IndexError, AttributeError):
            return None

    def split(self, *proportions):

        for prop in proportions:
            self.add_self()
            self.get_children()[-1].value = self.value * prop / sum(proportions)

    def round_leaves(self, min_diff=1):
        for leaf in self.traverse_leaves():
            factor = 1 / min_diff
            new_value = round(leaf.value * factor) / factor
            leaf.value = Fraction(new_value)

        difference = self.value - sum([leaf.value for leaf in self.traverse_leaves()])
        # if difference != 0:
        #     warnings.warn('tree node {} round leaves difference= {}'.format(self.__name__, difference))
        return difference

    def _reduce(self):
        sisters = self.get_siblings()

        if not sisters:
            raise Exception('no reduction possible without sisters')
        else:

            non_zero_sisters = [sister for sister in sisters if sister.value != 0]

            if non_zero_sisters:
                addition = Fraction(self.value, len(non_zero_sisters))
                for sister in non_zero_sisters:
                    if sister.value != 0:
                        sister.value += addition
                self.value = 0

    def reduce_children(self, condition):

        for child in self.get_children():
            if condition(child):
                child._reduce()

        to_be_detached = [child for child in self.get_children() if condition(child)]
        for child in to_be_detached:
            child.detach()

        self._children_fractal_values = [child.value for child in self.get_children()]

    def merge_children(self, *lengths):
        children = self.get_children()
        if not children:
            raise Exception('there are no children to be merged')
        if sum(lengths) != len(children):
            raise ValueError(
                'sum of lengths {} must be the same as length of children {}'.format(sum(lengths), len(children)))

        def _merge(nodes):
            node_value = [node.value for node in nodes]
            nodes[0].value = sum(node_value)
            for node in nodes[1:]:
                self.remove_child(node)

        iter_children = iter(children)
        chunks = [list(itertools.islice(iter_children, l)) for l in lengths]

        for chunk in chunks:
            _merge(chunk)

    def copy(self):
        return self.__class__(value=self.value, proportions=self.proportions,
                              tree_permutation_order=self.tree_permutation_order, multi=self.multi,
                              reading_direction=self.reading_direction, fertile=self.fertile)

    def __deepcopy__(self, memodict={}):
        copied = self.copy()
        copied._fractal_order = self.fractal_order
        copied.__name__ = self.__name__
        return copied
