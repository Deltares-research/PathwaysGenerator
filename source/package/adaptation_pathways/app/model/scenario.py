import dataclasses

from .metric import MetricValue


@dataclasses.dataclass
class TimeSeriesPoint:
    time: float
    data: MetricValue | None


@dataclasses.dataclass
class Scenario:
    id: str
    name: str
    metric_data_over_time: dict[int, dict[str, MetricValue]]

    def get_data(self, year: int, metric_id: str) -> MetricValue | None:
        if year not in self.metric_data_over_time:
            return None

        year_data = self.metric_data_over_time[year]
        if metric_id not in year_data:
            return None

        return year_data[metric_id]
