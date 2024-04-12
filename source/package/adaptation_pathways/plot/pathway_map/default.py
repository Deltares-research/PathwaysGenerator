import itertools

import matplotlib as mpl
import numpy as np

from ...graph import PathwayMap
from ...graph.node import ActionBegin, Node
from ..colour import PlotColours
from ..util import add_position, distribute, plot_graph, sort_horizontally
from .colour import default_colours


def _distribute_horizontally(
    pathway_map: PathwayMap,
    action_begin: ActionBegin,
    position_by_node: dict[Node, np.ndarray],
) -> None:
    assert isinstance(action_begin, ActionBegin)

    min_distance = 1.0
    begin_x = position_by_node[action_begin][0]

    action_end = pathway_map.action_end(action_begin)
    end_x = begin_x + min_distance

    # Push to the right if necessary
    if action_end in position_by_node:
        end_x = max(end_x, position_by_node[action_end][0])

    add_position(position_by_node, action_end, (end_x, np.nan))

    for action_begin_new in pathway_map.action_begins(
        pathway_map.action_end(action_begin)
    ):
        begin_x = end_x + min_distance

        # Push to the right if necessary
        if action_begin_new in position_by_node:
            begin_x = max(begin_x, position_by_node[action_begin_new][0])

        add_position(position_by_node, action_begin_new, (begin_x, np.nan))
        _distribute_horizontally(pathway_map, action_begin_new, position_by_node)


def _distribute_vertically(
    pathway_map: PathwayMap,
    action_begin: ActionBegin,
    position_by_node: dict[Node, np.ndarray],
) -> None:
    # Visit *all* action begins / ends in one go, in order of increasing x-coordinate
    # - Group action begins / ends by x-coordinate. Within each group:
    #     - Put each action end to position at the same height as its begin
    #     - For each action begin to position, take the mean y-coordinate of all
    #       incoming actions ends into account
    #     - Take some minimum distance into account. Move nodes that are too close to each other.

    assert isinstance(action_begin, ActionBegin)

    min_distance = 1.0
    nodes = pathway_map.all_action_begins_and_ends(action_begin)
    sorted_nodes, _ = sort_horizontally(nodes, position_by_node)

    # Iterate over sorted_nodes, grouped by their x-coordinate
    for _, grouped_sorted_nodes in itertools.groupby(  # type: ignore
        sorted_nodes,
        lambda action_begin_or_end: position_by_node[action_begin_or_end][0],
    ):
        nodes = list(grouped_sorted_nodes)

        # Initialize the y-coordinate with the mean of the y-coordinates of the nodes
        # that end in each node
        for node in nodes:
            # Each node is only visited once
            assert np.isnan(position_by_node[node][1])

            # Calculate the mean y-coordinate of actions that end in the to_action
            from_nodes = pathway_map.from_nodes(node)

            # Only the root node does not have from_nodes
            assert len(from_nodes) > 0

            y_coordinates = [position_by_node[node][1] for node in from_nodes]

            # All from_nodes must already be positioned
            assert all(
                not np.isnan(coordinate) for coordinate in y_coordinates
            ), from_nodes

            mean_y = sum(position_by_node[node][1] for node in from_nodes) / len(
                from_nodes
            )
            position_by_node[node][1] = mean_y

        # If the previous loop resulted in same / similar y-coordinates, we spread them
        # out some more
        y_coordinates = [position_by_node[node][1] for node in nodes]
        y_coordinates = distribute(list(y_coordinates), min_distance)

        for idx, node in enumerate(nodes):
            assert not np.isnan(position_by_node[node][1])
            position_by_node[node][1] = y_coordinates[idx]


def _layout(
    pathway_map: PathwayMap,
) -> dict[Node, np.ndarray]:
    """
    Layout for visualizing pathway maps

    :param pathway_map: Pathway map
    :return: Node positions

    The goal of this layout is to be able to visualize the contents of the graph.
    """
    position_by_node: dict[Node, np.ndarray] = {}

    if pathway_map.nr_edges() > 0:
        action_begin = pathway_map.root_node
        add_position(position_by_node, action_begin, (0, 0))

        _distribute_horizontally(pathway_map, action_begin, position_by_node)
        _distribute_vertically(pathway_map, action_begin, position_by_node)

    return position_by_node


def plot(
    axes: mpl.axes.Axes,
    pathway_map: PathwayMap,
    title: str = "",
    plot_colours: PlotColours | None = None,
) -> None:
    if plot_colours is None:
        plot_colours = default_colours(pathway_map)

    plot_graph(
        axes,
        pathway_map.graph,
        title,
        _layout(pathway_map),
        plot_colours,
    )
