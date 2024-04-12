from .action_period import ActionPeriod
from .node import Node


class ActionConversion(Node):
    """
    ActionConversion instances represent the moment that one action stops and another action
    begins

    :param from_action_period: Previous / old action period
    :param to_action_period: Next / new action period

    See also: :class:`PathwayMap`
    """

    def __init__(
        self, from_action_period: ActionPeriod, to_action_period: ActionPeriod
    ) -> None:
        super().__init__(f"{from_action_period} | {to_action_period}")
        self._from_action_period = from_action_period
        self._to_action_period = to_action_period

    def __repr__(self) -> str:
        return f'ActionConversion("{self._label}")'

    @property
    def from_action_period(self) -> ActionPeriod:
        return self._from_action_period

    @property
    def to_action_period(self) -> ActionPeriod:
        return self._to_action_period
