from enum import Enum


class MetricEstimate(Enum):
    MANUAL = 1
    SUM = 2
    AVERAGE = 3
    MINIMUM = 4
    MAXIMUM = 5
    LAST = 6


class MetricUnit:
    def __init__(self, symbol: str, place_after_value: bool, value_format: str):
        self.symbol = symbol
        self.place_after_value = place_after_value
        self.value_format = value_format

    def __eq__(self, other):
        if not isinstance(other, MetricUnit):
            return NotImplemented
        return (
            self.symbol == other.symbol
            and self.place_after_value == other.place_after_value
            and self.value_format == other.value_format
        )

    def __hash__(self):
        return hash((self.symbol, self.place_after_value, self.value_format))

    def __repr__(self):
        return f"MetricUnit(symbol={self.symbol}, place_after_value={self.place_after_value}, value_format={self.value_format})"


class Metric:
    def __init__(
        self,
        identifier: str,
        name: str,
        unit: MetricUnit,
        # current_value: float,
        estimate,
    ):
        self.id = identifier
        self.name = name
        self.unit = unit
        # self.current_value = current_value
        self.estimate = estimate

    def __eq__(self, other):
        if not isinstance(other, Metric):
            return NotImplemented
        return self.name == other.name if self.name else self.id == other.id

    def __hash__(self):
        return hash(self.name) if self.name else hash(self.id)

    def __repr__(self):
        return (
            f"Metric(id={self.id}, name={self.name}, unit={self.unit}, "
            # f"current_value={self.current_value}, "
            f"estimate={self.estimate})"
        )


class MetricValue:
    def __init__(self, value: float, is_estimate: bool):
        self.value = value
        self.is_estimate = is_estimate

    def __eq__(self, other):
        if not isinstance(other, MetricValue):
            return NotImplemented
        return self.value == other.value and self.is_estimate == other.is_estimate

    def __hash__(self):
        return hash((self.value, self.is_estimate))

    def __repr__(self):
        return f"MetricValue(value={self.value}, is_estimate={self.is_estimate})"
