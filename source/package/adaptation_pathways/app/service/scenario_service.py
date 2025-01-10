# pylint: disable=unused-argument,too-few-public-methods
from model.metric import Metric
from model.scenario import Scenario


class ScenarioService:
    @staticmethod
    def estimate_metric_at_time(
        metric: Metric, time: float, scenario: Scenario
    ) -> float:
        # Replace with a linear interpolation/extrapolation using the nearest points
        return 0
