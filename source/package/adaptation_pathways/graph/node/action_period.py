from ...action import Action
from .node import Node


class ActionPeriod(Node):
    """
    A node representing a period covered by an action

    :param action: Action this node represents

    See also: :class:`PathwayGraph`
    """

    _action: Action

    def __init__(self, action: Action) -> None:
        super().__init__(f"{action.name}")
        self._action = action

    def __repr__(self) -> str:
        return f'ActionPeriod("{self._action}")'

    @property
    def action(self) -> Action:
        return self._action
