from typing import TypeAlias

from ...action import Action
from .node import Node


TippingPoint: TypeAlias = int


class ActionEnd(Node):
    """
    :param action: Action this node is the end of
    :param tipping_point: Tipping point

    Tipping points are numerical values with unknown meaning. They may represent years or
    magnitudes of some environmental condition, for example.
    """

    _tipping_point: TippingPoint

    def __init__(self, action: Action, tipping_point: TippingPoint = 0) -> None:
        super().__init__(f"{action.name}]")
        self._action = action
        self._tipping_point = tipping_point

    def __repr__(self) -> str:
        return f'ActionEnd("{self._action}", {self._tipping_point})'

    @property
    def action(self) -> Action:
        return self._action

    @property
    def tipping_point(self) -> TippingPoint:
        return self._tipping_point

    @tipping_point.setter
    def tipping_point(self, tipping_point: TippingPoint) -> None:
        self._tipping_point = tipping_point
