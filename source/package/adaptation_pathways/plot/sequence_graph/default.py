import itertools

import matplotlib as mpl
import numpy as np

from ...graph import SequenceGraph
from ...graph.node.action import Action
from ..colour import PlotColours
from ..util import add_position, distribute, plot_graph, sort_horizontally
from ._colour import default_colours


def _distribute_horizontally(
    sequence_graph: SequenceGraph,
    from_action: Action,
    nodes: dict[Action, np.ndarray],
) -> None:
    min_distance = 1.0
    from_x = nodes[from_action][0]

    for to_action in sequence_graph.to_actions(from_action):
        to_x = from_x + min_distance

        # Push action to the right if necessary
        if to_action in nodes:
            to_x = max(to_x, nodes[to_action][0])

        add_position(nodes, to_action, (to_x, np.nan))

    for to_action in sequence_graph.to_actions(from_action):
        _distribute_horizontally(sequence_graph, to_action, nodes)


def _distribute_vertically(
    sequence_graph: SequenceGraph,
    from_action: Action,
    nodes: dict[Action, np.ndarray],
) -> None:
    # Visit *all* actions in one go, in order of increasing x-coordinate
    # - Group actions by x-coordinate. Within each group:
    #     - For each action to position, take the mean y-coordinates of all from-actions
    #       into account
    #     - Take some minimum distance into account. Move nodes that are too close to each other.

    min_distance = 1.0
    actions = sequence_graph.all_to_actions(from_action)
    sorted_actions, _ = sort_horizontally(actions, nodes)

    # Iterate over to_action_coordinate_pairs, grouped by their x-coordinate
    for _, grouped_sorted_actions in itertools.groupby(  # type: ignore
        sorted_actions, lambda action: nodes[action][0]
    ):
        actions = list(grouped_sorted_actions)

        # Initialize the y-coordinate with the mean of the y-coordinates of the from_actions
        # that end in each action
        for action in actions:
            # Each action is only visited once
            assert np.isnan(nodes[action][1]), f"action {action}: {nodes[action]}"

            # Calculate the mean y-coordinate of actions that end in the to_action
            from_actions = sequence_graph.from_actions(action)

            # Only the root action does not have from_actions
            assert len(from_actions) > 0

            y_coordinates = [nodes[action][1] for action in from_actions]

            # All from_actions must already be positioned
            assert all(not np.isnan(coordinate) for coordinate in y_coordinates)

            mean_y = sum(nodes[action][1] for action in from_actions) / len(
                from_actions
            )
            nodes[action][1] = mean_y

        # If the previous loop resulted in same / similar y-coordinates, we spread them
        # out some more
        y_coordinates = [nodes[action][1] for action in actions]
        y_coordinates = distribute(list(y_coordinates), min_distance)

        for idx, action in enumerate(actions):
            assert not np.isnan(nodes[action][1])
            nodes[action][1] = y_coordinates[idx]


def _layout(sequence_graph: SequenceGraph) -> dict[Action, np.ndarray]:
    """
    Layout for visualizing sequence graphs

    :param sequence_graph: Sequence graph
    :return: Node positions

    The goal of this layout is to be able to visualize the contents of the graph.
    """
    nodes: dict[Action, np.ndarray] = {}

    if sequence_graph.nr_actions() > 0:
        from_action = sequence_graph.root_node
        add_position(nodes, from_action, (0, 0))
        _distribute_horizontally(sequence_graph, from_action, nodes)
        _distribute_vertically(sequence_graph, from_action, nodes)

    return nodes


def plot(
    axes: mpl.axes.Axes,
    sequence_graph: SequenceGraph,
    title: str = "",
    plot_colours: PlotColours | None = None,
) -> None:
    if plot_colours is None:
        plot_colours = default_colours(sequence_graph)

    plot_graph(
        axes,
        sequence_graph.graph,
        title,
        _layout(sequence_graph),
        plot_colours,
    )
