import dataclasses

from metric import Metric, MetricValue


@dataclasses.dataclass
class TimeSeriesPoint:
    time: (
        float | None
    )  # js: A scenario might be provided or not. need to think about this
    data: MetricValue


@dataclasses.dataclass
class Scenario:
    id: str
    name: str
    metric_data_over_time: dict[Metric, list[TimeSeriesPoint]]
