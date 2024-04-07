"""
Action combinations are combinations of other actions. They are a special kind of action that
keeps track of which actions are combined. Code for visualizing graphs containing action
combinations can use this information to do things differently compared to regular actions.
"""

from .action import Action


class ActionCombination(Action):
    """
    ActionCombinations are represented by a name and by a collection of actions combined by
    this action

    :param name: Name of action. It is assumed that different actions have different names.
    :param actions: Collection of at least two actions combined.
    """

    _actions: list[Action]

    def __init__(self, name: str, actions: list[Action]) -> None:
        super().__init__(name)
        self._actions = list(dict.fromkeys(actions))

        if len(self._actions) < 2:
            raise ValueError("At least two different(!) actions must be combined")

    def __repr__(self) -> str:
        return f'ActionCombination("{self.name}", {self.actions})'

    @property
    def actions(self) -> list[Action]:
        return self._actions
