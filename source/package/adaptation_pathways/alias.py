"""
This module contains aliases to be used as type hints.
"""

from .action import Action
from .action_combination import ActionCombination


Actions = list[Action | ActionCombination]
Sequence = tuple[Action, Action]
Sequences = list[Sequence]
TippingPoint = float
TippingPointByAction = dict[Action, TippingPoint]
