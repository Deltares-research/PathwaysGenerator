from .comparisons import SequenceComparison
from .metric import Metric, MetricValue


class ActionDesign:
    def __init__(self, color: str, icon: str):
        self.color = color
        self.icon = icon

    def __eq__(self, other):
        if not isinstance(other, ActionDesign):
            return False
        return self.color == other.color and self.icon == other.icon

    def __hash__(self):
        return hash((self.color, self.icon))


class Action:
    def __init__(
        self,
        identifier: str,
        name: str,
        design: ActionDesign,
        metric_data: dict[Metric, MetricValue],
    ):
        self.id = identifier
        self.name = name
        self.design = design
        self.metric_data = metric_data  # dict[Metric, MetricValue | None]

    def __eq__(self, other):
        if not isinstance(other, Action):
            return NotImplemented
        return self.name == other.name if self.name else self.id == other.id

    def __hash__(self):
        return hash(self.name) if self.name else hash(self.id)

    def __repr__(self):
        return (
            f"Action(id={self.id}, name={self.name}, design={self.design}"
            f"metric_data={self.metric_data})"
        )


class ActionDependency:
    def __init__(
        self,
        identifier: str,
        action: Action,
        relation: SequenceComparison,
        other_actions: list,
        # actions_in_order: bool,
    ):
        self.id = identifier
        self.action = action
        self.relation = relation
        self.other_actions = other_actions  # list[Action]
        # self.actions_in_order = actions_in_order

    def __eq__(self, other):
        if not isinstance(other, ActionDependency):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return (
            f"ActionDependency(id={self.id}, action={self.action}, "
            f"relation={self.relation}, other_actions={self.other_actions}, "
            # f"actions_in_order={self.actions_in_order})"
        )
