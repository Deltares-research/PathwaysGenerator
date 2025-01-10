# pylint: disable=unused-argument
"""
Handles communication between the front-end app and backend code related to Pathways
"""

from model.action import Action
from model.filter import ActionFilter, GenerationConstraints, MetricFilter
from model.metric import Metric, MetricEstimate
from model.pathway import Pathway


class PathwayService:
    @staticmethod
    def filter_pathways(
        all_pathways: list[Pathway],
        action_filters: list[ActionFilter],
        metric_filters: list[MetricFilter],
    ) -> list[Pathway]:
        # Replace with actual filtering code
        return all_pathways

    @staticmethod
    def generate_pathways(
        current_situation: Action,
        all_actions: list[Action],
        all_metrics: list[Metric],
        constraints: GenerationConstraints,
    ) -> list[Pathway]:
        # Generate all pathways that don't violate the provided constraints
        # Estimate a value for each metric based on its Metric.estimate method
        return []
