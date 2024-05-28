from abc import ABC, abstractmethod
from typing import Optional

from musurgia.musurgia_exceptions import MarginNotSettableError, RelativePositionNotSettableError
from musurgia.musurgia_types import check_type


class _GetSlavePositionMixIn(ABC):
    @abstractmethod
    def get_slave_position(self, slave: 'PositionSlave', position: str) -> float:
        pass


class _GetSlaveMarginMixIn(ABC):
    @abstractmethod
    def get_slave_margin(self, slave: 'MarginSlave', margin: str) -> float:
        pass


class _SetSlavePositionMixIn:
    def __init__(self, relative_x: None = None, relative_y: None = None, *args, **kwargs):
        super().__init__(relative_x=relative_x, relative_y=relative_y, *args, **kwargs)

    @property
    def relative_x(self) -> float:
        return self.master.get_slave_position(slave=self, position='x')

    @relative_x.setter
    def relative_x(self, val: Optional[float]) -> None:
        if val is not None:
            raise RelativePositionNotSettableError()

    @property
    def relative_y(self) -> float:
        return self.master.get_slave_position(slave=self, position='y')

    @relative_y.setter
    def relative_y(self, val: Optional[float]) -> None:
        if val is not None:
            raise RelativePositionNotSettableError()


class _SetSlaveMarginMixIn:
    def __init__(self, left_margin: None = None, right_margin: None = None,
                 top_margin: None = None, bottom_margin: None = None, *args, **kwargs):
        super().__init__(left_margin=left_margin, right_margin=right_margin,
                         top_margin=top_margin, bottom_margin=bottom_margin, *args, **kwargs)

    @property
    def left_margin(self) -> float:
        return self.master.get_slave_margin(slave=self, margin='left')

    @left_margin.setter
    def left_margin(self, val: Optional[float]) -> None:
        if val is not None:
            raise MarginNotSettableError()

    @property
    def top_margin(self) -> float:
        return self.master.get_slave_margin(slave=self, margin='top')

    @top_margin.setter
    def top_margin(self, val: Optional[float]) -> None:
        if val is not None:
            raise MarginNotSettableError()

    @property
    def right_margin(self) -> float:
        return self.master.get_slave_margin(slave=self, margin='right')

    @right_margin.setter
    def right_margin(self, val: Optional[float]) -> None:
        if val is not None:
            raise MarginNotSettableError()

    @property
    def bottom_margin(self) -> float:
        return self.master.get_slave_margin(slave=self, margin='bottom')

    @bottom_margin.setter
    def bottom_margin(self, val: Optional[float]) -> None:
        if val is not None:
            raise MarginNotSettableError()


class _Named:
    def __init__(self, name: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name: Optional[str] = name

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, val: Optional[str]) -> None:
        if val is not None:
            check_type(val, str, class_name=self.__class__.__name__, property_name='name')
        self._name = val


class PositionMaster(_GetSlavePositionMixIn, ABC):
    pass


class MarginMaster(_GetSlaveMarginMixIn, ABC):
    pass


class Master(_GetSlavePositionMixIn, _GetSlaveMarginMixIn, ABC):
    pass


class PositionSlave(_Named, _SetSlavePositionMixIn):
    def __init__(self, master: Optional[PositionMaster] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._master: Optional[PositionMaster] = master

    @property
    def master(self) -> Optional[PositionMaster]:
        return self._master

    @master.setter
    def master(self, val: Optional[PositionMaster]) -> None:
        if val and not isinstance(val, PositionMaster):
            raise TypeError(f"master.value must be of type {PositionMaster} not {type(val)}")
        self._master = val


class MarginSlave(_Named, _SetSlaveMarginMixIn):
    def __init__(self, master: Optional[MarginMaster] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._master: Optional[MarginMaster] = master

    @property
    def master(self) -> Optional[MarginMaster]:
        return self._master

    @master.setter
    def master(self, val: Optional[MarginMaster]) -> None:
        if val and not isinstance(val, MarginMaster):
            raise TypeError(f"master.value must be of type {MarginMaster} not {type(val)}")
        self._master = val


class Slave(_Named, _SetSlavePositionMixIn, _SetSlaveMarginMixIn):
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
