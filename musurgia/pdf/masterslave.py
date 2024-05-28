from abc import ABC
from typing import Optional

from musurgia.musurgia_types import check_type


class SimpleNamed:
    def __init__(self, simple_name: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._simple_name: Optional[str] = simple_name

    @property
    def simple_name(self) -> Optional[str]:
        return self._simple_name

    @simple_name.setter
    def simple_name(self, val: Optional[str]) -> None:
        if val is not None:
            check_type(val, str, class_name=self.__class__.__name__, property_name='simple_name')
        self._simple_name = val


class Master(ABC):
    pass


class Slave(SimpleNamed):
    def __init__(self, master: Optional[Master] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._master: Optional[Master] = master

    @property
    def master(self) -> Optional[Master]:
        return self._master

    @master.setter
    def master(self, val: Optional[Master]) -> None:
        if val and not isinstance(val, Master):
            raise TypeError(f"master.value must be of type {Master} not {type(val)}")
        self._master = val
