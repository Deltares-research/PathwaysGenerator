"""
An action instance is a synonym for policy action, intervention, and measure, for example
which has a unique set of preceding actions. The instance signifies that the timing of an action
can be different depending on which measures have been implemented before
"""

from .app.model.action import Action
from .app.model.metric import Metric, MetricValue


class ActionInstance:
    def __init__(
        self,
        action: Action,
        instance: int,
        tipping_point: float,
        metric_data: dict[Metric, MetricValue | None],
    ):
        self.action = action
        self.instance = instance
        self.tipping_point = tipping_point
        self.metric_data = metric_data

    def __eq__(self, other):
        if not isinstance(other, ActionInstance):
            return NotImplemented
        return (
            self.action == other.action
            and self.instance == other.instance
            and self.tipping_point == other.tipping_point
        )

    def __hash__(self):
        return hash((self.action, self.instance, self.tipping_point))

    def __repr__(self):
        return (
            f"ActionInstance(action={self.action}, instance={self.instance}, "
            f"tipping_point={self.tipping_point}, metric_data={self.metric_data})"
        )
