import dataclasses

from action import Action
from metric import Metric, MetricValue


@dataclasses.dataclass
class Pathway:
    id: str
    base_action: Action
    child_pathways: list["Pathway"]
    metric_data: dict[Metric, MetricValue]
