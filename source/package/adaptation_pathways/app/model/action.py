import dataclasses

from .comparisons import SequenceComparison
from .metric import MetricEffect


@dataclasses.dataclass
class Action:
    id: str
    name: str
    color: str
    icon: str
    metric_data: dict[str, MetricEffect]

    def apply_effect(self, metric_id: str, value: float) -> float:
        if metric_id not in self.metric_data:
            return value

        effect = self.metric_data[metric_id]
        return effect.apply_to(value)


@dataclasses.dataclass
class ActionDependency:
    id: str
    action: Action
    relation: SequenceComparison
    other_actions: list[Action]
    actions_in_order: bool
