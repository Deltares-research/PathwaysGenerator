from .node import ActionBegin, ActionEnd, ActionPeriod
from .node.action import Action as ActionNode
from .pathway_graph import PathwayGraph
from .pathway_map import PathwayMap
from .sequence_graph import SequenceGraph


def sequence_graph_to_pathway_graph(sequence_graph: SequenceGraph) -> PathwayGraph:
    """
    Convert a sequence graph to a pathway graph
    """

    def visit_graph(
        sequence_graph: SequenceGraph,
        pathway_graph: PathwayGraph,
        from_action: ActionNode,
        new_from_action: ActionPeriod,
    ) -> None:
        for to_action in sequence_graph.to_actions(from_action):
            new_to_action = ActionPeriod(to_action.action)
            pathway_graph.add_conversion(new_from_action, new_to_action)
            visit_graph(sequence_graph, pathway_graph, to_action, new_to_action)

    pathway_graph = PathwayGraph()

    if sequence_graph.nr_actions() > 0:
        from_action = sequence_graph.root_node
        assert isinstance(from_action, ActionNode), from_action
        new_from_action = ActionPeriod(from_action.action)

        visit_graph(sequence_graph, pathway_graph, from_action, new_from_action)

    return pathway_graph


def pathway_graph_to_pathway_map(pathway_graph: PathwayGraph) -> PathwayMap:
    """
    Convert a pathway graph to a pathway map
    """

    def visit_graph(
        pathway_graph: PathwayGraph,
        pathway_map: PathwayMap,
        action_period: ActionPeriod,
        action_ends: dict[ActionNode, ActionEnd],
    ) -> ActionBegin:
        begin = ActionBegin(action_period.action)
        end = ActionEnd(action_period.action)

        pathway_map.add_period(begin, end)

        for conversion in pathway_graph.to_conversions(action_period):
            begin_new = visit_graph(
                pathway_graph,
                pathway_map,
                pathway_graph.to_action_period(conversion),
                action_ends,
            )
            pathway_map.add_conversion(end, begin_new)

        return begin

    pathway_map = PathwayMap()

    if pathway_graph.nr_nodes() > 0:
        action_period = pathway_graph.root_node
        action_ends: dict[ActionNode, ActionEnd] = {}
        visit_graph(pathway_graph, pathway_map, action_period, action_ends)

    return pathway_map


def sequence_graph_to_pathway_map(sequence_graph: SequenceGraph) -> PathwayMap:
    """
    Convert a sequence graph to a pathway map

    This function calls :func:`sequence_graph_to_pathway_graph` and
    :func:`pathway_graph_to_pathway_map` in turn.
    """
    return pathway_graph_to_pathway_map(sequence_graph_to_pathway_graph(sequence_graph))
