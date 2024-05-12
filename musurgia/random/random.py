from typing import Optional

from musurgia.utils import check_type, MusurgiaTypeError, NonNegativeInteger

__all__ = ['Random']


class Random:
    """
    .. code-block:: python

        from musurgia.random import Random

    Random is a class for creating pseudo random series of values. Values are chosen from a list of values
    called a 'pool' which does not contain any duplicates. The property 'periodicity' defines the minimum number of
    other values which must be given out before a value can appear again.

    >>> first = Random(pool=[1, 3, 2, 4, 5], periodicity=2, seed=20)
    >>> second = Random(pool=[1, 3, 2, 4, 5], periodicity=2, seed=20)
    >>> [first.__next__() for _ in range(20)]
    [3, 2, 1, 5, 3, 1, 4, 3, 2, 4, 5, 3, 2, 4, 1, 5, 4, 1, 3, 5]
    >>> [second.__next__() for _ in range(20)]
    [3, 1, 2, 3, 5, 1, 2, 3, 5, 1, 2, 3, 5, 4, 3, 2, 5, 4, 3, 1]
    >>> second.periodicity = 1
    >>> [second.__next__() for _ in range(20)]
    [3, 5, 4, 2, 3, 1, 5, 1, 5, 3, 4, 3, 1, 2, 1, 2, 4, 5, 1, 3]
    >>> second.periodicity = 0
    >>> [second.__next__() for _ in range(20)]
    [1, 4, 5, 2, 1, 1, 5, 1, 1, 2, 2, 1, 2, 1, 1, 3, 3, 5, 5, 1]

    """
    import random
    current_random = random

    def __init__(self, pool, periodicity=None, forbidden_list=None, seed=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pool = None
        self._periodicity = None
        self._forbidden_list = None
        self._seed = None
        self._counter = 0
        self._previous_elements = []

        self.pool = pool
        self.periodicity = periodicity
        self.forbidden_list = forbidden_list
        self.seed = seed

    # properties
    @property
    def counter(self) -> NonNegativeInteger:
        """
        Keeps track of the number of times :obj:`permutation_order_iterator` is called

        :return: NonNegativeInteger

        >>> r = Random(pool=['a', 'b', 'c'], periodicity=1, seed=20)
        >>> r.counter
        0
        >>> next(r)
        'c'
        >>> r.counter
        1
        >>> next(r)
        'a'
        >>> r.counter
        2
        """
        return self._counter

    @property
    def forbidden_list(self) -> list:
        """
        Set and get ``forbidden_list`` property which is used internally to keep trace of previous elements and has
        maximum length of :obj:`periodicity`. All elements in this list are forbidden to be chosen from. After
        randomly choose a permitted element, this will be added to the forbidden list and the first element of this
        list will be removed. This is a naive mechanism which guaranties the appropriate distance between two
        appearances of an element according for :obj:`periodicity`

        The ``forbidden_list`` can also be set manually. In this case if its length is larger than
        :obj:`periodicity`, :obj:`permutation_order_iterator` will remove so many elements from the beginning of this list until the
        right length is achieved.

        >>> Random(pool=[1, 2, 3], forbidden_list="[2]")
        Traceback (most recent call last):
            ...
        TypeError: Random.forbidden_list: Value [2] must be of type list not str.
        >>> r = Random(pool=[1, 3, 2, 4, 5, 6], periodicity=4, seed=20, forbidden_list=[2, 3, 1])
        >>> previous_forbidden_list = r.forbidden_list[:]
        >>> el1 = next(r)
        >>> el1 not in previous_forbidden_list
        True
        >>> r.forbidden_list == [2, 3, 1] + [el1]
        True
        >>> previous_forbidden_list = r.forbidden_list[:]
        >>> el2 = next(r)
        >>> el2 not in previous_forbidden_list
        True
        >>> r.forbidden_list == [3, 1] + [el1, el2]
        True
        >>> previous_forbidden_list = r.forbidden_list[:]
        >>> el3 = next(r)
        >>> el3 not in previous_forbidden_list
        True
        >>> r.forbidden_list == [1] + [el1, el2, el3]
        True
        """
        if not self._forbidden_list:
            self._forbidden_list = []
        return self._forbidden_list

    @forbidden_list.setter
    def forbidden_list(self, values: Optional[list]):
        if values is not None:
            try:
                check_type(t=list, v=values, class_name=self.__class__.__name__, property_name='forbidden_list')
            except MusurgiaTypeError as err:
                raise TypeError(err.msg)
        self._forbidden_list = values

    @property
    def periodicity(self) -> Optional['NonNegativeInteger']:
        """
        Set and get ``periodicity`` property of types ``None`` or ``NonNegativInteger``. This property defines the
        minimum distance between two appearances of an element.
        If set to ``0`` immediate repetitions are permitted,
        if set to ``1`` at least one other element must be given out before this element can be chosen again an so on.
        If set to ``len(self.pool) - 1`` a random permutation of elements will be repeated.

        If set to ``None``, ``len(self.pool) - 2`` is returned. If len(self.pool) is ``1``, ``0`` is returned.
        If set to a value equal or greater than ``len(self.pool)``, ``len(self.pool) - 1`` is returned.

        >>> Random(pool=[1, 2, 3], periodicity=-1)
        Traceback (most recent call last):
           ...
        TypeError: Random.periodicity: Value -1 must be of type NonNegativeInteger not int.

        >>> Random(pool=[1, 2, 3], periodicity=1.6)
        Traceback (most recent call last):
           ...
        TypeError: Random.periodicity: Value 1.6 must be of type NonNegativeInteger not float.

        >>> Random(pool=[1, 2, 3, 4]).periodicity
        2
        >>> Random(pool=[1]).periodicity
        0
        >>> Random(pool=[1, 2, 3, 4], periodicity=5).periodicity
        3

        """
        if self.pool:
            if self._periodicity is None:
                output = len(self.pool) - 2
                return output if output >= 0 else 0

            if self._periodicity >= len(self.pool):
                return len(self.pool) - 1
        return self._periodicity

    @periodicity.setter
    def periodicity(self, value: Optional[int]):
        if value is not None:
            try:
                check_type(t=NonNegativeInteger, v=value, property_name='periodicity',
                           class_name=self.__class__.__name__)
                self._periodicity = value
            except MusurgiaTypeError as err:
                raise TypeError(err.msg)

    @property
    def pool(self) -> list:
        """
        Set and get ``pool`` property. This property defines the list of possible elements to be randomly chosen from.
        Duplicates will be omitted without chaining the order of each element's first appearances.
        :return: ``None`` or ``list``

        >>> Random(pool=3)
        Traceback (most recent call last):
            ...
        ValueError: Random.pool must be iterable.

        >>> Random(pool=None)
        Traceback (most recent call last):
            ...
        ValueError: Random.pool must be iterable.

        >>> Random(pool=[1, 2, 3, 2, 1]).pool
        [1, 2, 3]
        """
        return self._pool

    @pool.setter
    def pool(self, values):
        if not hasattr(values, '__iter__'):
            raise ValueError('Random.pool must be iterable.')
        self._pool = list(dict.fromkeys(values))

    @property
    def seed(self):
        """
        Set and get ``seed.a`` value of python random function which is used to randomly choose an element.

        .. seealso:: https://docs.python.org/3/library/random.html#random.seed

        >>> Random(pool=[1, 2, 3], periodicity=0).seed

        >>> Random(pool=[1, 2, 3], periodicity=0, seed=10).seed
        10
        >>> Random(pool=[1, 2, 3], periodicity=0, seed='Can be a string too').seed
        'Can be a string too'
        """
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value
        self.current_random.seed(value)

    # methods
    def get_previous_elements(self) -> list:
        """
        :return: list of all randomly chosen values

        >>> r = Random(pool=[1, 3, 2, 4, 5], periodicity=2, seed=20)
        >>> [r.__next__() for _ in range(20)]
        [3, 2, 1, 5, 3, 1, 4, 3, 2, 4, 5, 3, 2, 4, 1, 5, 4, 1, 3, 5]
        >>> r.get_previous_elements()
        [3, 2, 1, 5, 3, 1, 4, 3, 2, 4, 5, 3, 2, 4, 1, 5, 4, 1, 3, 5]
        """
        return self._previous_elements

    def __iter__(self):
        """
        The core methode of Random. This is a generator to generate random values. :obj:`__next__` method calls :obj:`__iter__().__next__()`.

        :return: a random value out of :obj:`pool` considering :obj:`seed`, :obj:`periodicity` and :obj:`forbidden_list`
        """
        while True:
            def check(element):
                def forbid_element(el):
                    if len(self.forbidden_list) >= self.periodicity:
                        self.forbidden_list.pop(0)
                    self.forbidden_list.append(el)

                if self.periodicity != 0:
                    if element in self.forbidden_list:
                        return False
                    else:
                        forbid_element(element)
                        return True
                else:
                    return True

            if len(self.forbidden_list) > self.periodicity:
                self.forbidden_list = self.forbidden_list[(-1 * self.periodicity):]

            random_element = self.pool[self.current_random.randrange(len(self.pool))]
            while check(random_element) is False:
                random_element = self.pool[self.current_random.randrange(len(self.pool))]
            self._counter += 1
            self._previous_elements.append(random_element)
            yield random_element

    def __next__(self):
        """
        :return: self.__iter__().__next__()`
        """
        return self.__iter__().__next__()

    def __deepcopy__(self, memodict={}):
        copied = self.__class__(pool=self.pool, periodicity=self.periodicity,
                                forbidden_list=self.forbidden_list,
                                seed=self.seed)
        return copied
