from ...action import Action
from .node import Node


class ActionBegin(Node):
    """
    A node representing the begin of an action

    An action covers a period of time. This node represents the start of this period.

    :param action: Action this node is the begin of

    See also: :class:`PathwayMap`
    """

    _action: Action

    def __init__(self, action: Action) -> None:
        super().__init__(f"[{action.name}")
        self._action = action

    def __repr__(self) -> str:
        return f'ActionBegin("{self._action}")'

    @property
    def action(self) -> Action:
        return self._action
