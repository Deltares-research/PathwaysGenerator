"""
A sequence is an ordered list of actions.
"""

import dataclasses

from .app.model.action import Action
from .app.model.metric import Metric, MetricValue


@dataclasses.dataclass()
class SequenceFilter:
    is_valid: bool
    filtered_out: bool
    reasoning: str


class Sequence:
    def __init__(
        self,
        actions: list[Action],
        performance: dict[Metric, MetricValue],
        filters: SequenceFilter,
    ):
        self.actions = actions
        self.performance = performance
        self.filters = filters

    def __eq__(self, other):
        if not isinstance(other, Sequence):
            return NotImplemented
        return self.actions == other.actions and self.performance == other.performance

    def __hash__(self):
        # Hash based on actions and performance
        return hash((tuple(self.actions), frozenset(self.performance.items())))

    def __repr__(self):
        return (
            f"Sequence(actions={self.actions}, performance={self.performance}, "
            f"filters={self.filters}"
        )
