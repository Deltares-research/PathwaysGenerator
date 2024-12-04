import dataclasses
from enum import Enum


class MetricEstimate(Enum):
    MANUAL = 1
    SUM = 2
    AVERAGE = 3
    MINIMUM = 4
    MAXIMUM = 5
    LAST = 6


@dataclasses.dataclass
class MetricUnit:
    symbol: str
    place_after_value: bool
    value_format: str


@dataclasses.dataclass
class Metric:
    id: str
    name: str
    unit: MetricUnit
    current_value: (
        float  # js: is this needed? Metric is usually paired with MetricValue?
    )
    estimate: MetricEstimate


@dataclasses.dataclass
class MetricValue:
    value: float
    is_estimate: bool
