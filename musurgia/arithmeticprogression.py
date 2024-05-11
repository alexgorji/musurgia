from quicktions import Fraction


class ArithmeticProgressionError(BaseException):
    def __init__(self, *args):
        super().__init__(*args)


class DAndSError(ArithmeticProgressionError):
    """
    >>> ArithmeticProgression(d=4, an=15, s=33)
    Traceback (most recent call last):
        ...
    musurgia.arithmeticprogression.DAndSError: you cannot set both d an s!

    """

    def __init__(self, *args):
        msg = 'you cannot set both d an s!'
        super().__init__(msg, *args)


class ArithmeticProgression(object):
    """

    """

    def __init__(self, a1=None, an=None, n=None, d=None, s=None, correct_s=False):
        self._a1 = None
        self._an = None
        self._n = None
        self._d = None
        self._s = None
        self._current = None
        self._index = None
        self._correction_factor = None
        self._correct_s = None

        self.a1 = a1
        self.an = an
        self.n = n
        self.d = d
        self.s = s
        self.correct_s = correct_s

    # private methods

    def _check_args(self, arg=None):
        if arg is None:
            err = 'Not enough attributes are set. Three are needed!'
            if len([v for v in self._get_private_parameters_dict().values() if v is not None]) < 3:
                raise AttributeError(err)
        else:
            if self._get_private_parameters_dict()[arg] is None and len(
                    [v for v in self._get_private_parameters_dict().values() if v is not None]) > 2:
                err = 'attribute cannot be set. Three parameters are already set. ArithmeticProgression is already ' \
                      'created!'
                raise AttributeError(err)

    def _calculate_a1(self):
        if self._d is None:
            self._a1 = Fraction(2 * self.s, self.n) - self.an
        else:
            self._a1 = self.an - ((self.n - 1) * self.d)

    def _calculate_an(self):
        if self._s is None:
            self._an = self.a1 + (self.n - 1) * self.d
        else:
            self._an = Fraction(2 * self.s, self.n) - self.a1

    def _calculate_n(self):
        if self._s is None:
            self._n = Fraction((self.an - self.a1), self.d) + 1
        else:
            self._n = 2 * Fraction(self.s, (self.a1 + self.an))
        self._n = int(self._n)

    def _calculate_d(self):
        if self.n == 1:
            self._d = 0
        elif self._a1 is None:
            self._calculate_a1()
            self._d = Fraction((self.an - self.a1), (self.n - 1))
        elif self._an is None:
            self._d = Fraction(((self.s - (self.n * self.a1)) * 2), ((self.n - 1) * self.n))
        elif self._n is None:
            self._calculate_n()
            self._d = Fraction((self.an - self.a1), (self.n - 1))
        else:
            self._d = Fraction((self.an - self.a1), (self.n - 1))

    def _calculate_s(self):
        if self._a1 is None:
            self._calculate_a1()
            self._s = (self.a1 + self.an) * Fraction(self.n, 2)
        elif self._an is None:
            self._s = self.n * self.a1 + ((self.n - 1) * Fraction(self.n, 2)) * self.d
        elif self._n is None:
            self._calculate_n()
            self._s = (self.a1 + self.an) * Fraction(self.n, 2)
        else:
            self._s = (self.a1 + self.an) * Fraction(self.n, 2)

    def _get_private_parameters_dict(self):
        return {'a1': self._a1, 'an': self._an, 'n': self._n, 'd': self._d, 's': self._s}

    def _to_fraction(self, value):
        if not isinstance(value, Fraction):
            value = Fraction(value)
        return value

    # public properties

    @property
    def a1(self):
        """
        >>> arith = ArithmeticProgression(n=3, an=15, d=4)
        >>> arith.a1
        Fraction(7, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]


        >>> arith = ArithmeticProgression(n=3, an=15, s=33)
        >>> arith.a1
        Fraction(7, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]


        :return:
        """
        if self._a1 is None:
            self._calculate_a1()
        return self._a1

    @a1.setter
    def a1(self, value):
        if value is not None:
            value = self._to_fraction(value)
            self._check_args('a1')
        self._a1 = value

    @property
    def an(self):
        """
        >>> arith = ArithmeticProgression(n=3, a1=7, d=4)
        >>> arith.an
        Fraction(15, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        >>> arith = ArithmeticProgression(n=3, a1=7, s=33)
        >>> arith.an
        Fraction(15, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        :return:
        """
        if self._an is None:
            self._calculate_an()
        return self._an

    @an.setter
    def an(self, value):
        if value is not None:
            value = self._to_fraction(value)
            self._check_args('an')
        self._an = value

    @property
    def correct_s(self):
        """
        >>> arith = ArithmeticProgression(a1= 3, an=6, s=21)
        >>> arith.get_parameters_dict()
        {'a1': Fraction(3, 1), 'an': Fraction(6, 1), 'n': 4, 'd': Fraction(1, 1), 's': Fraction(21, 1)}
        >>> arith.get_actual_s()
        Fraction(18, 1)
        >>> result = list(arith)
        >>> result
        [Fraction(3, 1), Fraction(4, 1), Fraction(5, 1), Fraction(6, 1)]
        >>> sum(result)
        Fraction(18, 1)

        >>> arith.correct_s = True
        >>> arith.reset_iterator()
        >>> arith.get_correction_factor()
        Fraction(7, 6)
        >>> result = list(arith)
        >>> result
        [Fraction(7, 2), Fraction(14, 3), Fraction(35, 6), Fraction(7, 1)]
        >>> sum(result)
        Fraction(21, 1)

        """
        return self._correct_s

    @correct_s.setter
    def correct_s(self, val):
        if not isinstance(val, bool):
            raise TypeError(f'correct_s.value must be of type bool not{val.__class__.__name__}')
        self._correct_s = val
        self._correction_factor = None

    @property
    def d(self):
        """"
        >>> arith = ArithmeticProgression(a1= 7, an=15, s=33)
        >>> arith.d
        Fraction(4, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        >>> arith = ArithmeticProgression(a1= 7, an=15, n=3)
        >>> arith.d
        Fraction(4, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        >>> arith = ArithmeticProgression(a1= 7, n=3, s=33)
        >>> arith.d
        Fraction(4, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        >>> arith = ArithmeticProgression(an= 15, n=3, s=33)
        >>> arith.d
        Fraction(4, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]
        """
        if self._d is None:
            self._calculate_d()
        return self._d

    @d.setter
    def d(self, value):
        if value is not None:
            value = self._to_fraction(value)
            self._check_args('d')
            if self._s is not None:
                raise DAndSError()
        self._d = value

    @property
    def n(self):
        """
        >>> arith = ArithmeticProgression(an=15, a1=7, d=4)
        >>> arith.n
        3
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        >>> arith = ArithmeticProgression(an=15, a1=7, s=33)
        >>> arith.n
        3
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        :return:
        """

        if self._n is None:
            self._calculate_n()
        return self._n

    @n.setter
    def n(self, value):
        if value is not None:
            if not isinstance(value, int):
                raise AttributeError('n {} must be int'.format(value))
            self._check_args('n')
        self._n = value

    @property
    def s(self):
        """
        >>> arith = ArithmeticProgression(a1= 7, an=15, d=4)
        >>> arith.s
        Fraction(33, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        >>> arith = ArithmeticProgression(a1= 7, an=15, n=3)
        >>> arith.s
        Fraction(33, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        >>> arith = ArithmeticProgression(a1= 7, n=3, d=4)
        >>> arith.s
        Fraction(33, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        >>> arith = ArithmeticProgression(an= 15, n=3, d=4)
        >>> arith.s
        Fraction(33, 1)
        >>> list(arith)
        [Fraction(7, 1), Fraction(11, 1), Fraction(15, 1)]

        """

        if self._s is None:
            self._calculate_s()
        return self._s

    @s.setter
    def s(self, value):
        if value is not None:
            value = self._to_fraction(value)
            self._check_args('s')
            if self._d is not None:
                raise DAndSError()
        self._s = value

    # public methods

    def get_actual_s(self):
        return self.n * Fraction((self.a1 + self.an), 2)

    def get_correction_factor(self):
        def _calculate_correction_factor():
            if self.correct_s:
                return Fraction(self.s, self.get_actual_s())
            else:
                return 1

        if self._correction_factor is None:
            self._correction_factor = _calculate_correction_factor()
        return self._correction_factor

    def get_current_index(self):
        """
        >>> arith = ArithmeticProgression(a1=1, d=2, n=3)
        >>> arith.get_current_index()
        >>> next(arith)
        Fraction(1, 1)
        >>> arith.get_current_index()
        0
        >>> next(arith)
        Fraction(3, 1)
        >>> arith.get_current_index()
        1
        >>> next(arith)
        Fraction(5, 1)
        >>> arith.get_current_index()
        2
        >>> next(arith)
        Traceback (most recent call last):
            ...
        StopIteration
        >>> arith.get_current_index()
        2
        """
        return self._index

    def get_parameters_dict(self):
        """
        >>> ArithmeticProgression(n=15, a1=1, d=2).get_parameters_dict()
        {'a1': Fraction(1, 1), 'an': Fraction(29, 1), 'n': 15, 'd': Fraction(2, 1), 's': Fraction(225, 1)}

        :return:
        """
        return {'a1': self.a1, 'an': self.an, 'n': self.n, 'd': self.d, 's': self.s}

    def reset_iterator(self):
        self._current = None
        self._index = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._current is None:
            self._check_args()
        parameters = [self.a1, self.an, self.n, self.s, self.d]

        if len([v for v in parameters if v is not None]) < 5:
            err = 'Not enough parameter set to create an arithmetic progression. 3 parameters should be set first (s ' \
                  'and d cannot be set together) '
            raise Exception(err)

        if self._current is None:
            self._current = self.a1
            self._index = 0
        else:
            if self._index + 1 >= self.n:
                raise StopIteration()
            self._index += 1
            self._current += self.d

        return self._current * self.get_correction_factor()

    def __deepcopy__(self, memodict={}):
        copy = self.__class__(correct_s=self.correct_s)
        copy._a1 = self._a1
        copy._an = self._an
        copy._n = self._n
        copy._d = self._d
        copy._s = self._s
        return copy
