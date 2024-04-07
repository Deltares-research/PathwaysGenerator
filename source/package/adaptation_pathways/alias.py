"""
This module contains aliases to be used as type hints.
"""

from .action import Action
from .action_combination import ActionCombination
from .plot.alias import *  # pylint: disable=wildcard-import, unused-wildcard-import


Actions = list[Action | ActionCombination]
Sequence = tuple[Action, Action]
Sequences = list[Sequence]
TippingPoint = int
TippingPointByAction = dict[Action, TippingPoint]
