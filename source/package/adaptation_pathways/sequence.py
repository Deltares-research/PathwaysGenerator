"""
A sequence is an ordered list of actions.
"""

import dataclasses

from app.model.action import Action
from app.model.metric import Metric, MetricValue


@dataclasses.dataclass
class Sequence:
    actions: list[Action]
    performance: dict[Metric, MetricValue | None]
    is_valid: bool = False  # Tracks whether the sequence is valid
    filtered_out: bool = True  # Tracks whether sequence is considered after filtering
    exclusion_reason: str = (
        "None"  # Additional information (e.g., reasons for filtering)
    )
