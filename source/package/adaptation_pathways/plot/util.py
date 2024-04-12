"""
This module contains utilities used for plotting graphs
"""

import itertools
import typing

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from ..action import Action
from .colour import PlotColours


def init_axes(axes: mpl.axes.Axes) -> None:
    """
    Initializes the axes

    Spines and ticks are hidden.
    """

    axes.spines.top.set_visible(False)
    axes.spines.right.set_visible(False)
    axes.spines.bottom.set_visible(False)
    axes.spines.left.set_visible(False)
    axes.tick_params(
        left=False,
        bottom=False,
    )
    axes.set_xticklabels([])
    axes.set_yticklabels([])


def plot_graph(
    axes: mpl.axes.Axes,
    graph: nx.DiGraph,
    title: str,
    layout: dict[typing.Any, np.ndarray],
    plot_colours: PlotColours,
) -> None:
    """
    Plot the graph using NetworkX plotting routines
    """
    title = title.strip()

    if len(title) > 0:
        axes.set_title(title)

    nx.draw_networkx_edges(
        graph,
        ax=axes,
        pos=layout,
        edge_color=plot_colours.edge_colours,
        width=1.0,
        arrows=False,
    )

    nx.draw_networkx_nodes(
        graph,
        ax=axes,
        pos=layout,
        node_color=plot_colours.node_colours,
        node_size=250,
        linewidths=0.5,
        edgecolors=plot_colours.node_edge_colours,
    )

    nx.draw_networkx_labels(
        graph,
        ax=axes,
        pos=layout,
        font_size="medium",
        font_weight="bold",
        verticalalignment="bottom",
        horizontalalignment="right",
        font_color=plot_colours.label_colour,
    )


def save_plot(pathname: str) -> None:
    """
    Save the current matplotlib plot to a file

    Transparency will be set.
    """
    plt_options = {
        # "bbox_inches": "tight",
        "transparent": True,
    }
    plt.savefig(pathname, **plt_options)


def _unsort_idxs(values: list[typing.Any]) -> list[int]:
    # Actually, the type of value must be "Comparable" (not "Any") but there is no built-in
    # support for that yet in Python
    idxs = list(range(len(values)))
    idxs.sort(key=values.__getitem__, reverse=True)

    return idxs


def _sort(values: list[float]) -> tuple[list[float], list[int]]:
    return list(sorted(values, reverse=True)), _unsort_idxs(values)


def _unsort(values: list[float], idxs: list[int]) -> list[float]:
    original_ordered_values = [0.0] * len(values)

    for idx, value in zip(idxs, values):
        original_ordered_values[idx] = value

    return original_ordered_values


def add_position(
    position_by_node: dict[typing.Any, np.ndarray],
    node: typing.Any,
    position: tuple[float, float],
) -> None:
    """
    Add position of a node to the collection

    Note that the collection passed in is updated.
    """
    position_by_node[node] = np.array(position, np.float64)


def sort_horizontally(
    nodes: list[typing.Any], position_by_node: dict[typing.Any, np.ndarray]
) -> tuple[list[typing.Any], list[float]]:
    """
    Sort all nodes by x-coordinate and return the sorted nodes and their x-coordinates
    """
    sorted_nodes: list[typing.Any] = []
    x_coordinates = []

    if len(nodes) > 0:
        x_coordinates = [position_by_node[node][0] for node in nodes]
        action_coordinate_pairs = sorted(
            zip(nodes, x_coordinates), key=lambda pair: pair[1]
        )
        sorted_nodes, x_coordinates = (list(it) for it in zip(*action_coordinate_pairs))

    return sorted_nodes, x_coordinates


def distribute(coordinates: list[float], min_distance: float) -> list[float]:
    """
    Distribute the coordinates in such a way that the difference between each coordinate is
    at least greater or equal to a certain distance

    :param coordinates: List of coordinates
    :param min_distance: Minimum distance between two consecutive coordinates
    :return: List of coordinates satisfying the minimum distance criterion. If additional space is
        added between the coordinates, this is added evenly to both sides of the range of
        coordinates.
    """
    coordinates, idxs = _sort(coordinates)

    assert sorted(coordinates, reverse=True) == coordinates, coordinates
    assert min_distance >= 0

    distributed_coordinates = []

    if len(coordinates) <= 1:
        distributed_coordinates = coordinates
    if len(coordinates) > 1:
        distances = []

        for lhs, rhs in itertools.pairwise(coordinates):
            current_distance = rhs - lhs
            if current_distance < min_distance:
                distances.append(current_distance)

        if len(distances) == 0:
            distributed_coordinates = coordinates
        else:
            distance_to_add = (len(distances) * min_distance) - sum(distances)
            half_distance_to_add = 0.5 * distance_to_add
            offset = -half_distance_to_add

            for lhs, rhs in itertools.pairwise(coordinates):
                current_distance = rhs - lhs
                lhs += offset

                if current_distance < min_distance:
                    offset += min_distance - current_distance

                distributed_coordinates.append(lhs)

            distributed_coordinates.append(coordinates[-1] + offset)

    distributed_coordinates = _unsort(distributed_coordinates, idxs)

    return list(reversed(distributed_coordinates))


def action_level_by_first_occurrence(
    sequences: list[tuple[Action, Action]]
) -> dict[Action, float]:
    """
    Determine a level per action the sequences of actions passed in

    The returned collection of levels can be used for vertically ordering actions in graphs. The
    levels are based on the order in which the actions are mentioned in the input collection.
    Actions occurring earlier in the collection, are assigned lower levels.
    """
    level_by_action: dict[Action, float] = {}

    for idx, (from_action, to_action) in enumerate(sequences, 1):
        if from_action not in level_by_action:
            level_by_action[from_action] = idx + 0.01
        if to_action not in level_by_action:
            level_by_action[to_action] = idx - 0.01

    return level_by_action
