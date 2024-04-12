class Node:
    """
    Base class for specialized node types

    Nodes are nodes in a graph.

    :param label: Label of the node
    """

    _label: str

    def __init__(self, label: str) -> None:
        self._label = label

    def __str__(self) -> str:
        return self._label

    def __repr__(self) -> str:
        return f'Node("{self._label}")'

    @property
    def label(self) -> str:
        return self._label
