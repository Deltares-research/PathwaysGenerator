from .action import Action
from .comparisons import NumberComparison, SequenceComparison
from .metric import Metric


class ActionFilter:
    def __init__(
        self,
        relation: SequenceComparison,
        actions: list[Action],
        actions_in_order: bool,
    ):
        self.relation = relation
        self.actions = actions
        self.actions_in_order = actions_in_order

    def __eq__(self, other):
        if not isinstance(other, ActionFilter):
            return NotImplemented
        return (
            self.relation == other.relation
            and self.actions == other.actions
            and self.actions_in_order == other.actions_in_order
        )

    def __hash__(self):
        return hash((self.relation, tuple(self.actions), self.actions_in_order))

    def __repr__(self):
        return (
            f"ActionFilter(relation={self.relation}, actions={self.actions}, "
            f"actions_in_order={self.actions_in_order})"
        )


class MetricFilter:
    def __init__(self, metric: Metric, relation: NumberComparison, value: float):
        self.metric = metric
        self.relation = relation
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, MetricFilter):
            return NotImplemented
        return (
            self.metric == other.metric
            and self.relation == other.relation
            and self.value == other.value
        )

    def __hash__(self):
        return hash((self.metric, self.relation, self.value))

    def __repr__(self):
        return f"MetricFilter(metric={self.metric}, relation={self.relation}, value={self.value})"


class GenerationConstraints:
    def __init__(
        self,
        action_constraints: list[ActionFilter],
        metric_constraints: list[MetricFilter],
        max_sequence_length: int | None = None,
    ):
        self.action_constraints = action_constraints
        self.metric_constraints = metric_constraints
        self.max_sequence_length = max_sequence_length

    def __eq__(self, other):
        if not isinstance(other, GenerationConstraints):
            return NotImplemented
        return (
            self.action_constraints == other.action_constraints
            and self.metric_constraints == other.metric_constraints
            and self.max_sequence_length == other.max_sequence_length
        )

    def __hash__(self):
        return hash(
            (
                tuple(self.action_constraints),
                tuple(self.metric_constraints),
                self.max_sequence_length,
            )
        )

    def __repr__(self):
        return (
            f"GenerationConstraints(action_constraints={self.action_constraints}, "
            f"metric_constraints={self.metric_constraints}, "
            f"max_sequence_length={self.max_sequence_length})"
        )
