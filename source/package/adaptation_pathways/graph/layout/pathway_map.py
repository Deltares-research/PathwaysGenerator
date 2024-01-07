import itertools

import numpy as np

from ..node import ActionBegin, Node
from ..pathway_map import PathwayMap
from .util import add_position, distribute, sort_horizontally


def _default_distribute_horizontally(
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
        _default_distribute_horizontally(
            pathway_map, action_begin_new, position_by_node
        )


def _default_distribute_vertically(
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


def default_layout(
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

        _default_distribute_horizontally(pathway_map, action_begin, position_by_node)
        _default_distribute_vertically(pathway_map, action_begin, position_by_node)

    return position_by_node


def _classic_distribute_horizontally(
    pathway_map: PathwayMap,
    action_begin: ActionBegin,
    position_by_node: dict[Node, np.ndarray],
) -> None:
    assert isinstance(action_begin, ActionBegin)

    action_end = pathway_map.action_end(action_begin)
    end_x = action_end.tipping_point

    add_position(position_by_node, action_end, (end_x, np.nan))

    for action_begin_new in pathway_map.action_begins(
        pathway_map.action_end(action_begin)
    ):
        begin_x = end_x

        add_position(position_by_node, action_begin_new, (begin_x, np.nan))
        _classic_distribute_horizontally(
            pathway_map, action_begin_new, position_by_node
        )


def _classic_distribute_vertically(
    pathway_map: PathwayMap,
    root_action_begin: ActionBegin,
    position_by_node: dict[Node, np.ndarray],
) -> None:
    action_end = pathway_map.action_end(root_action_begin)
    position_by_node[action_end][1] = position_by_node[root_action_begin][1]

    min_distance = 1.0
    actions = [
        action for action in pathway_map.actions() if action != root_action_begin.action
    ]
    y_coordinates = [float(position_by_node[root_action_begin][1])] * len(actions)
    y_coordinates = distribute(y_coordinates, min_distance)

    if len(y_coordinates) % 2 == 1:
        y_coordinates = [
            coordinate + 0.5 * min_distance for coordinate in y_coordinates
        ]

    y_coordinate_by_action = dict(zip(actions, y_coordinates))

    for action_begin in pathway_map.all_action_begins():
        y_coordinate = y_coordinate_by_action[action_begin.action]

        assert np.isnan(position_by_node[action_begin][1])
        position_by_node[action_begin][1] = y_coordinate
        action_end = pathway_map.action_end(action_begin)

        assert np.isnan(position_by_node[action_end][1])
        position_by_node[action_end][1] = y_coordinate


def classic_layout(
    pathway_map: PathwayMap,
) -> dict[Node, np.ndarray]:
    """
    Layout that replicates the pathway map layout of the original (pre-2024) pathway generator

    :param pathway_map: Pathway map
    :return: Node positions

    The layout has the following characteristics:

    - A pathway map is a stack of horizontal lines representing actions
    - Each action ends up at its own level in the stack
    - Pathways jump from horizontal line to horizontal line, depending on the sequences of
      actions that make up each pathway

    The pathway map passed in must contain sane tipping points. When in doubt, call
    ``verify_tipping_points()`` before calling this function.
    """
    position_by_node: dict[Node, np.ndarray] = {}

    if pathway_map.nr_edges() > 0:
        root_action_begin = pathway_map.root_node
        root_action_end = pathway_map.action_end(root_action_begin)
        tipping_point = root_action_end.tipping_point

        min_tipping_point, max_tipping_point = pathway_map.tipping_point_range()
        tipping_point_range = max_tipping_point - min_tipping_point
        assert tipping_point_range > 0
        x_coordinate = tipping_point - 0.1 * tipping_point_range

        add_position(position_by_node, root_action_begin, (x_coordinate, 0))

        _classic_distribute_horizontally(
            pathway_map, root_action_begin, position_by_node
        )
        _classic_distribute_vertically(pathway_map, root_action_begin, position_by_node)

    return position_by_node