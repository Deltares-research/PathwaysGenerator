from ..action import Action
from .node.action import Action as ActionNode
from .rooted_graph import RootedGraph


class SequenceGraph(RootedGraph):
    """
    A SequenceGraph represents the dependencies between actions. Each node represents an action,
    and each edge the fact that one action follows another one.
    """

    def __init__(self, sequences: list[tuple[Action, Action]] | None = None) -> None:
        """
        Create a sequence graph, based on a collection of sequences

        Each of the actions in the sequences passed in is associated with a node in the graph.
        The same action is associated with the same node.
        """
        super().__init__()

        if sequences is not None:
            node_by_action: dict[Action, ActionNode] = {}

            for from_action, to_action in sequences:
                self.add_sequence(
                    node_by_action.setdefault(from_action, ActionNode(from_action)),
                    node_by_action.setdefault(to_action, ActionNode(to_action)),
                )

    def add_action(self, action: ActionNode) -> None:
        """
        Add an action

        :param action: ActionNode
        """
        self._graph.add_node(action)

    def add_sequence(self, from_action: ActionNode, to_action: ActionNode) -> None:
        """
        Add a sequence of actions

        :param from_action: First action of the sequence
        :param to_action: Second action of the sequence
        """
        self._graph.add_edge(from_action, to_action)

    def add_sequences(self, actions: list[tuple[ActionNode, ActionNode]]) -> None:
        """
        Add sequences of actions

        :param actions: List of tuples of ``from_action`` and ``to_action``
        """
        return self._graph.add_edges_from(actions)

    def nr_actions(self) -> int:
        """
        :return: Number of actions (nodes)
        """
        return self.nr_nodes()

    def nr_from_actions(self, to_action: ActionNode) -> int:
        """
        :return: Number of sequences that end at the action passed in

        In graph-speek, this is the action's in-degree.
        """
        return self._graph.in_degree(to_action)

    def from_actions(self, to_action: ActionNode) -> list[ActionNode]:
        """
        :return: Collection of actions that end at the action passed in
        """
        return self.from_nodes(to_action)

    def nr_to_actions(self, from_action: ActionNode) -> int:
        """
        :return: Number of sequences that start at the action passed in

        In graph-speek, this is the action's out-degree.
        """
        return self._graph.out_degree(from_action)

    def to_actions(self, from_action: ActionNode) -> list[ActionNode]:
        """
        :return: Collection of actions that start at the action passed in
        """
        return self.to_nodes(from_action)

    def nr_sequences(self) -> int:
        """
        :return: Number of sequences
        """
        return len(self._graph.edges)

    def all_to_actions(self, from_action: ActionNode) -> list[ActionNode]:
        return self.all_to_nodes(from_action)
