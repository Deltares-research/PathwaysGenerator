from .metric import Metric, MetricValue


class Pathway:
    id: str
    action_id: str
    parent_id: str | None = None
    metric_data: dict[str, MetricValue]

    def __init__(
        self,
        action_id: str,
        parent_id: str | None = None,
    ):
        self.id = action_id if parent_id is None else f"{parent_id}->{action_id}"
        self.action_id = action_id
        self.parent_id = parent_id
        self.metric_data = {}

    def get_formatted_value(self, metric: Metric) -> str:
        data = self.metric_data.get(metric.id, None)
        if data is None:
            return ""

        return metric.unit.format(data.value)
