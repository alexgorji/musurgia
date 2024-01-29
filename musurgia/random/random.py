from typing import Optional, TypeAlias

from musurgia.random.errors import RandomPoolError, RandomPeriodicityError

__all__ = ['Random']

from musurgia.utils import check_type, MusurgiaTypeError

NonNegativeInteger: TypeAlias = int


class Random:
    """
    .. code-block:: python

        from musurgia.random import Random

    Random is a class for creating pseudo random series of elements. Elements are chosen from a list of elements
    called a 'pool' which does not contain any duplicates. The property 'periodicity' defines the minimum number of
    other elements which must be given out before an element can appear again.


    """
    import random
    current_random = random

    def __init__(self, pool=None, periodicity=None, forbidden_list=None, seed=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pool = None
        self._periodicity = None
        self._forbidden_list = None
        self._seed = None
        self._counter = 0
        self._result = None

        self.pool = pool
        self.periodicity = periodicity
        self.forbidden_list = forbidden_list
        self.seed = seed

    # periodicity None will sets the periodicity always to len(pool)-2
    @property
    def pool(self) -> Optional[list]:
        """
        Set and get ``pool`` property. This property defines the list of possible elements to be randomly chosen from.
        Duplicates will be omitted without chaining the order of each element's first appearances.
        :return: ``None`` or ``list``
        """
        return self._pool

    @pool.setter
    def pool(self, values):
        if values is not None and not hasattr(values, '__iter__'):
            raise RandomPoolError('Random.pool must be iterable.')
        if values is not None:
            self._pool = list(dict.fromkeys(values))

    @property
    def periodicity(self) -> Optional['NonNegativeInteger']:
        """
        Set and get ``periodicity`` property of types ``None`` or ``non-negative int``. This property defines the
        minimum distance between two appearances of an element.
        If set to ``0`` immediate repetitions are permitted,
        if set to ``1`` at least one other element must be given out before this element can be chosen again an so on.
        If set to ``len(self.pool) - 1`` a random permutation of elements will be repeated.

        If set to ``None``, ``len(self.pool) - 2`` is returned. If len(self.pool) is ``1``, ``0`` is returned.
        If set to a value equal or greater than ``len(self.pool)``, ``len(self.pool) - 1`` is returned.
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
                check_type(t='non_negative_int', v=value, argument_name='value', method_name='periodicity', obj=self)
                self._periodicity = value
            except MusurgiaTypeError as err:
                raise RandomPeriodicityError(err.msg)

    @property
    def forbidden_list(self) -> list:
        """
        Set and get ``forbidden_list`` property which is used internally to keep trace of previous elements and has
        maximum length of :obj:`periodicity`. All elements in this list are forbidden to be chosen from. After
        randomly choose a permitted element, this will be added to the forbidden list and the first element of this
        list will be removed. This is a naive mechanism which guaranties the appropriate distance between two
        appearances of an element according for :obj:`periodicity`

        The ``forbidden_list`` can also be set manually. In this case if its length is larger than
        :obj:`periodicity`, :obj:`iterator` will remove so many elements from the beginning of this list until the
        right length is achieved.
        """
        if not self._forbidden_list:
            self._forbidden_list = []
        return self._forbidden_list

    @forbidden_list.setter
    def forbidden_list(self, values: Optional[list]):
        self._forbidden_list = values

    @property
    def seed(self):
        """
        Get and set ``seed`` of python random which is used to randomly choose an element.
        """
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value
        self.current_random.seed(value)

    @property
    def counter(self):
        return self._counter

    @property
    def result(self):
        if self._result is None:
            self._result = []
        return self._result

    @property
    def iterator(self):
        if not self.pool:
            raise RandomPoolError('pool is not set!')
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

            yield random_element

    def __iter__(self):
        return self.iterator

    def __next__(self):
        next_el = self.iterator.__next__()
        self._counter += 1
        self.result.append(next_el)

        return next_el

    def __deepcopy__(self, memodict={}):
        copied = self.__class__(pool=self.pool, periodicity=self.periodicity,
                                forbidden_list=self.forbidden_list,
                                seed=self.seed)
        return copied
