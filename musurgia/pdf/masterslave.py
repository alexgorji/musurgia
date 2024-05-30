# from abc import ABC, abstractmethod
# from typing import Optional, Any, Union, Protocol
#
# from musurgia.musurgia_exceptions import RelativePositionNotSettableError, MarginNotSettableError
# from musurgia.musurgia_types import check_type, MusurgiaTypeError
# from musurgia.pdf.margined import Margined, AbstractMargined
# from musurgia.pdf.positioned import Positioned, AbstractPositioned
#
#
# class SlavePositionGetter(ABC):
#     @abstractmethod
#     def get_slave_position(self, slave: 'PositionedSlave', position: str) -> float:
#         """get_slave_position must be provided"""
#
#
# class SlaveMarginGetter(ABC):
#     @abstractmethod
#     def get_slave_margin(self, slave: 'MarginedSlave', margin: str) -> float:
#         """get_slave_margin must be provided"""
#
# #
# # class Master(ABC):
# #     pass
# #
# #
# # class PositionedMaster(Positioned, SlavePositionGetter, ABC):
# #     pass
# #
# #
# # class MarginedMaster(Margined, SlaveMarginGetter, ABC):
# #     pass
# #
# #
# # class MarginedPositionedMaster(MarginedMaster, PositionedMaster, ABC):
# #     pass
#
#
# class HasMasterProtocol(Protocol):
#     @property
#     def master(self) -> Union[MarginedMaster, PositionedMaster]: ...
#
#
# class PositionedSlave(AbstractPositioned, HasMasterProtocol):
#     @property
#     def relative_x(self) -> float:
#         return self.master.get_slave_position(slave=self, position='x')
#
#     @relative_x.setter
#     def relative_x(self, val: Optional[float]) -> None:
#         if val is not None:
#             raise RelativePositionNotSettableError()
#
#     @property
#     def relative_y(self) -> float:
#         return self.master.get_slave_position(slave=self, position='y')
#
#     @relative_y.setter
#     def relative_y(self, val: Optional[float]) -> None:
#         if val is not None:
#             raise RelativePositionNotSettableError()
#
#
# class MarginedSlave(AbstractMargined, HasMasterProtocol):
#     @property
#     def left_margin(self) -> float:
#         return self.master.get_slave_margin(slave=self, margin='left')
#
#     @left_margin.setter
#     def left_margin(self, val: Optional[float]) -> None:
#         if val is not None:
#             raise MarginNotSettableError()
#
#     @property
#     def top_margin(self) -> float:
#         return self.master.get_slave_margin(slave=self, margin='top')
#
#     @top_margin.setter
#     def top_margin(self, val: Optional[float]) -> None:
#         if val is not None:
#             raise MarginNotSettableError()
#
#     @property
#     def right_margin(self) -> float:
#         return self.master.get_slave_margin(slave=self, margin='right')
#
#     @right_margin.setter
#     def right_margin(self, val: Optional[float]) -> None:
#         if val is not None:
#             raise MarginNotSettableError()
#
#     @property
#     def bottom_margin(self) -> float:
#         return self.master.get_slave_margin(slave=self, margin='bottom')
#
#     @bottom_margin.setter
#     def bottom_margin(self, val: Optional[float]) -> None:
#         if val is not None:
#             raise MarginNotSettableError()
#
#
# # class SimpleNamed:
# #     def __init__(self, simple_name: Optional[str] = None, *args: Any, **kwargs: Any):
# #         super().__init__(*args, **kwargs)
# #         self._simple_name = None
# #         self.simple_name = simple_name
# #
# #     @property
# #     def simple_name(self) -> Optional[str]:
# #         return self._simple_name
# #
# #     @simple_name.setter
# #     def simple_name(self, val: Optional[str]) -> None:
# #         if val is not None:
# #             check_type(val, str, class_name=self.__class__.__name__, property_name='simple_name')
# #         self._simple_name = val
# #
# #
# # class Slave(SimpleNamed):
# #     def __init__(self, master: Optional[Master] = None, *args: Any, **kwargs: Any):
# #         super().__init__(*args, **kwargs)
# #         self._master = None
# #         self.master = master
# #
# #     @property
# #     def master(self) -> Optional[Master]:
# #         return self._master
# #
# #     @master.setter
# #     def master(self, val: Optional[Master]) -> None:
# #         # if val and not isinstance(val, Master):
# #         #     raise MusurgiaTypeError(message=f"master.value must be of type {Master} not {type(val)}",
# #         #                             class_name=self.__class__.__name__, property_name='master')
# #         self._master = val
