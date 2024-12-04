"""
An action instance is a synonym for policy action, intervention, and measure, for example
which has a unique set of preceding actions. The instance signifies that the timing of an action
can be different depending on which measures have been implemented before
"""

import dataclasses

from app.model.action import Action
from app.model.metric import Metric, MetricValue


@dataclasses.dataclass
class ActionInstance:
    action: Action
    instance: int
    tipping_point: float
    metric_data: dict[Metric, MetricValue | None]
