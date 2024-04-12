"""
This module contains aliases to be used as type hints.
"""

from ..action import Action
from .colour import Colour, Colours  # pylint: disable=unused-import


ColourByAction = dict[Action, Colour]
ColourByActionName = dict[str, Colour]
