from pathlib import Path
from pprint import pprint
from typing import Optional

import matplotlib as mpl
from matplotlib._afm import AFM


class FontError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def _make_afm_path_dictionary():
    def check_entry():
        old_afm = output.get((family, weight, style))
        if old_afm is not None:
            old_header = old_afm._header
            new_header = afm._header
            diff = set(old_header) ^ set(new_header)
            if diff == {b'CapHeight'}:
                if new_header.get(b'CapHeight'):
                    return True
            elif diff == set():
                return False
            else:
                raise AttributeError(
                    f'{family}, {weight}, {style} already in dict: {old_afm} differnce: {diff}')
        else:
            return True

    output = {}
    directory = Path(mpl.get_data_path(), 'fonts', 'afm')
    for file in directory.iterdir():
        afm_path = file
        with afm_path.open('rb') as fh:
            afm = AFM(fh)
        family = afm.get_familyname()
        weight = afm.get_weight().lower()
        if afm.get_angle() < 0:
            style = 'italic'
        else:
            style = 'regular'
        if check_entry():
            output[family, weight, style] = afm

    return output


class Font:
    """
    Class representing a font. It is used in class Text to set font family, weight, style and size.
    It accesses matplotlib._afm.AFM class (Adobe Font Metrics) to be able to determine the exact height and width of
    the text in pixels via two methods: :obj:`get_text_pixel_height()` and :obj:`get_text_pixel_width()`

    Attributes:
        family: Default value is ``Helvetica``.
        weight: Default value is ``medium``
        style: Default value is ``regular``
        size: Default value is `10`
    """

    __AFM_PATH_DICTIONARY = _make_afm_path_dictionary()
    # pprint(__AFM_PATH_DICTIONARY)
    _FAMILY = ['Courier']
    _WEIGHT = ['bold', 'medium']
    _STYLE = ['italic', 'regular']

    def __init__(self, family: str = 'Courier', weight: str = 'medium', style: str = 'regular', size: int = 10, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._family = None
        self._weight = None
        self._style = None
        self._size = None
        self._afm: Optional[AFM] = None

        self.family = family
        self.weight = weight
        self.style = style
        self.size = size

    def _set_afm(self):
        if self.family and self.weight and self.style:
            self._afm = self.__AFM_PATH_DICTIONARY[self.family, self.weight, self.style]

    @property
    def family(self):
        """
        Set and get font family. Currently valid values are [``Helvetica``, ``Courier``, ``Times``]
        """
        return self._family

    @family.setter
    def family(self, val):
        if val not in self._FAMILY:
            raise FontError(f'{val} not a valid value: Current valid families are: :obj:~{self._FAMILY}')
        self._family = val
        self._set_afm()

    @property
    def size(self):
        """
        Set and get font size
        """
        return self._size

    @size.setter
    def size(self, val):
        self._size = val

    @property
    def style(self):
        """
        Set and get font style. Valid values are [``italic``, ``regular``]
        """
        return self._style

    @style.setter
    def style(self, val):
        if val not in self._STYLE:
            raise FontError(f'{val} not a valid value: {self._STYLE}')
        self._style = val
        self._set_afm()

    @property
    def weight(self):
        """
        Set and get font weight. Valid values are [``bold``, ``medium``]
        """
        return self._weight

    @weight.setter
    def weight(self, val):
        if val not in self._WEIGHT:
            raise FontError(f'{val} not a valid value: {self._WEIGHT}')
        self._weight = val
        self._set_afm()

    def get_text_pixel_width(self, val: str) -> float:
        """
        :param val: text as str
        :return: width of text in pixels

        >>> Font().get_text_pixel_width('Test')
        18.25
        >>> Font(size=12).get_text_pixel_width('Test')
        21.9
        """
        if self._afm is None:
            raise TypeError()
        return (self._afm.string_width_height(val)[0] / 1000) * self.size

    def get_text_pixel_height(self, val: str) -> float:
        """
        :param val: text as str
        :return: height of text in pixels

        >>> Font().get_text_pixel_height('Test')
        7.33
        >>> Font(size=12).get_text_pixel_height('Test')
        8.796
        >>> Font(size=12, weight='bold', style='italic').get_text_pixel_height('Test')
        8.783999999999999
        """
        if self._afm is None:
            raise TypeError()
        return (self._afm.string_width_height(val)[1] / 1000) * self.size
