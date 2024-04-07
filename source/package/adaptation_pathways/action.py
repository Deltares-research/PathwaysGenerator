"""
An action is a synonym for policy action, intervention, and measure, for example.
"""


class Action:
    """
    Actions are simply represented by a name

    :param name: Name of the action. It is assumed that different actions have different names.
    """

    _name: str

    def __init__(self, name: str) -> None:
        self._name = name

    def __str__(self) -> str:
        return f"{self._name}"

    def __repr__(self) -> str:
        return f'Action("{self._name}")'

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name
