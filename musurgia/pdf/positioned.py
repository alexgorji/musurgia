from abc import abstractmethod, ABC
from typing import Optional, Protocol, Union, Any, cast

from musurgia.musurgia_exceptions import RelativePositionNotSettableError
from musurgia.musurgia_types import ConvertibleToFloat, check_type


class AbstractPositioned(ABC):
    """
    An interface for setting and getting DrawObject's position attributes.
    """

    def __init__(self, relative_x: Optional[ConvertibleToFloat] = None, relative_y: Optional[ConvertibleToFloat] = None,
                 *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._relative_x: float = 0
        self._relative_y: float = 0
        self.relative_x = relative_x  # type: ignore
        self.relative_y = relative_y  # type: ignore

    @property
    @abstractmethod
    def relative_x(self) -> float:
        raise NotImplementedError

    @relative_x.setter
    @abstractmethod
    def relative_x(self, val: Optional[ConvertibleToFloat]) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def relative_y(self) -> float:
        raise NotImplementedError

    @relative_y.setter
    @abstractmethod
    def relative_y(self, val: Optional[ConvertibleToFloat]) -> None:
        raise NotImplementedError

    def get_positions(self) -> dict[str, float]:
        return {'x': self.relative_x, 'y': self.relative_y}


class Positioned(AbstractPositioned):
    def __init__(self, relative_x: ConvertibleToFloat = 0, relative_y: ConvertibleToFloat = 0, *args: Any,
                 **kwargs: Any):
        super().__init__(relative_x=relative_x, relative_y=relative_y, *args, **kwargs)  # type: ignore

    @property
    def relative_x(self) -> float:
        return self._relative_x

    @relative_x.setter
    def relative_x(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='relative_x')
        self._relative_x = float(val)

    @property
    def relative_y(self) -> float:
        return self._relative_y

    @relative_y.setter
    def relative_y(self, val: ConvertibleToFloat) -> None:
        check_type(val, 'ConvertibleToFloat', class_name=self.__class__.__name__, property_name='relative_y')
        self._relative_y = float(val)


class PositionedMaster(Positioned, ABC):
    @abstractmethod
    def get_slave_position(self, slave: 'PositionedSlave', position: str) -> float:
        pass


class HasPositionedMasterProtocol(Protocol):
    @property
    def master(self) -> 'PositionedMaster': ...


class PositionedSlave(AbstractPositioned, HasPositionedMasterProtocol):
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
