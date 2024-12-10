from .metric import Metric, MetricValue


class TimeSeriesPoint:
    def __init__(self, time: float | None, data: MetricValue):
        self.time = time
        self.data = data

    def __eq__(self, other):
        if not isinstance(other, TimeSeriesPoint):
            return NotImplemented
        return self.time == other.time and self.data == other.data

    def __hash__(self):
        return hash((self.time, self.data))

    def __repr__(self):
        return f"TimeSeriesPoint(time={self.time}, data={self.data})"


class Scenario:
    def __init__(
        self,
        identifier: str,
        name: str,
        metric_data_over_time: dict[Metric, list[TimeSeriesPoint]],
    ):
        self.id = identifier
        self.name = name
        self.metric_data_over_time = metric_data_over_time

    def __eq__(self, other):
        if not isinstance(other, Scenario):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return (
            f"Scenario(id={self.id}, name={self.name}, "
            f"metric_data_over_time={self.metric_data_over_time})"
        )
