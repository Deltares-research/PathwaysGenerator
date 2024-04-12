from ..action import Action
from ..action_combination import ActionCombination
from .node import ActionBegin, ActionEnd
from .rooted_graph import RootedGraph


class PathwayMap(RootedGraph):
    """
    A PathwayMap represents a collection of adaptation pathways. These pathways are encoded
    in a directed rooted graph in which the nodes represent...
    """

    def add_period(self, begin: ActionBegin, end: ActionEnd) -> None:
        assert isinstance(begin, ActionBegin)
        assert isinstance(end, ActionEnd)
        self.graph.add_edge(begin, end)

    def add_conversion(self, end: ActionEnd, begin: ActionBegin) -> None:
        assert isinstance(end, ActionEnd)
        assert isinstance(begin, ActionBegin)
        self.graph.add_edge(end, begin)

    def action_begins(self, end: ActionEnd) -> list[ActionBegin]:
        assert isinstance(end, ActionEnd)
        return list(self.graph.adj[end])

    def action_end(self, begin: ActionBegin) -> ActionEnd:
        assert isinstance(begin, ActionBegin)
        ends = list(self.graph.adj[begin])
        assert len(ends) == 1
        return ends[0]

    def all_action_begins_and_ends(
        self, begin: ActionBegin
    ) -> list[ActionBegin | ActionEnd]:
        assert isinstance(begin, ActionBegin)
        return self.all_to_nodes(begin)

    def all_action_begins(self) -> list[ActionBegin]:
        assert isinstance(self.root_node, ActionBegin)

        result = [self.root_node]

        for node in self.all_to_nodes(self.root_node):
            if isinstance(node, ActionBegin):
                result.append(node)

        return result

    def all_action_ends(self) -> list[ActionEnd]:
        assert isinstance(self.root_node, ActionBegin)

        result = []

        for node in self.all_to_nodes(self.root_node):
            if isinstance(node, ActionEnd):
                result.append(node)

        return result

    def actions(self) -> list[Action]:
        return (
            list(dict.fromkeys(begin.action for begin in self.all_action_begins()))
            if self.nr_nodes() > 0
            else []
        )

    def continued_actions(self, action_combination: ActionCombination) -> list[Action]:
        """
        Return the actions that are continued by the ``action_combination``, if any
        """
        result = []

        # Find node in map containing the action combination passed in

        action_begin: ActionBegin | None = None

        for action_begin in self.all_action_begins():
            if action_begin.action.name == action_combination.name:
                # Current action begin contains the action combination

                for action_end, _ in self.graph.in_edges(action_begin):
                    assert isinstance(action_end, ActionEnd)
                    if action_end.action.name in [
                        action.name for action in action_combination.actions
                    ]:
                        result.append(action_end.action)

        return result

    def action_ends_by_action(self, action: Action) -> list[ActionEnd]:
        """
        Return ``ActionEnd`` nodes associated with the action passed in

        :raises LookupError: In case no ``ActionEnd`` node can be found that is associated with
            the action
        """
        assert isinstance(action, Action), type(action)
        result = []

        for node in self.graph.nodes:
            if isinstance(node, ActionEnd) and node.action == action:
                result.append(node)

        if len(result) == 0:
            raise LookupError(f"Action {action} is not part of the pathway map")

        return result

    def assign_tipping_points(
        self, tipping_points: dict[Action, int], verify: bool = False
    ) -> None:
        """
        Assign / update tipping points to ActionEnd nodes associated with the actions passed in

        :param verify: Whether or not the tipping points should be checked for consistency,
            using :py:func:`verify_tipping_points`
        """
        for action, tipping_point in tipping_points.items():
            for action_end in self.action_ends_by_action(action):
                action_end.tipping_point = tipping_point

        if verify:
            verify_tipping_points(self)

    def tipping_points(self) -> list[int]:
        """
        Return all unique tipping points, in increasing order
        """
        result: list[int] = []

        for action_end in self.all_action_ends():
            result.append(action_end.tipping_point)

        return list(dict.fromkeys(result))

    def tipping_point_range(self) -> tuple[int, int]:
        result = (0, 0)

        if self.nr_nodes() > 0:
            min_tipping_point = self.action_end(self.root_node).tipping_point
            max_tipping_point = min_tipping_point

            for end_node in self.leaf_nodes():
                max_tipping_point = max(max_tipping_point, end_node.tipping_point)

            result = (min_tipping_point, max_tipping_point)

        assert result[0] <= result[1], result

        return result

    # def set_node_attribute(self, name: str, value: dict[Action, typing.Any]) -> None:
    #     """
    #     Add / update attribute to / of those nodes that are associated with the actions passed in

    #     :param name: Name of attribute to set
    #     :param value: Per action a value of the attribute to set

    #     The caller is responsible of assuring that all nodes get assigned an attribute value.
    #     """
    #     for node in self.graph.nodes:
    #         if node.action in value:
    #             self.graph.nodes[node][name] = value[node.action]


def verify_tipping_points(pathway_map: PathwayMap) -> None:
    """
    Verify all tipping points in the pathway map passed in are correctly set

    :raises ValueError: In case one or more tipping points are not correctly set

    Tipping points are correct if they strictly increase along the sequences of actions.
    """

    for paths in pathway_map.all_paths():
        # [begin, end, begin, end, ...]

        tipping_point_from = paths[1].tipping_point

        for idx in range(3, len(paths), 2):
            tipping_point_to = paths[idx].tipping_point

            if tipping_point_to < tipping_point_from:
                raise ValueError(
                    f"Given the sequences of actions, the tipping point of action "
                    f"{paths[idx].action} ({tipping_point_to}) "
                    f"must be equal or larger than {tipping_point_from}"
                )

            tipping_point_from = tipping_point_to
