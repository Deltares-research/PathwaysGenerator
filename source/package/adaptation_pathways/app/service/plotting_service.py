# pylint: disable=too-few-public-methods,unused-argument
"""
Methods for drawing charts and graphs
"""
from typing import Any

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from adaptation_pathways.action import Action
from adaptation_pathways.alias import Sequence, TippingPointByAction
from adaptation_pathways.app.model.pathways_project import PathwaysProject
from adaptation_pathways.graph.convert import sequence_graph_to_pathway_map
from adaptation_pathways.graph.node.action import Action as ActionNode
from adaptation_pathways.graph.sequence_graph import SequenceGraph
from adaptation_pathways.plot import init_axes, plot_classic_pathway_map
from adaptation_pathways.plot.util import action_level_by_first_occurrence


matplotlib.use("svg")


class PlottingService:
    @staticmethod
    def draw_metro_map(
        project: PathwaysProject, for_export=False
    ) -> tuple[Figure, Axes]:

        action_nodes: dict[str, ActionNode] = {}
        tipping_points: TippingPointByAction = {}
        action_colors: dict[str, str] = {}
        metric = project.graph_metric

        # Create action node for each pathway
        for pathway in project.sorted_pathways:
            pathway_action = project.get_action(pathway.action_id)
            action = Action(pathway_action.name)
            action_node = ActionNode(action)
            action_nodes[pathway.id] = action_node
            action_colors[action.name] = pathway_action.color

            metric_value = pathway.metric_data.get(metric.id, None)
            value = metric.current_value if metric_value is None else metric_value.value
            tipping_points[action] = value

        # Populate sequences
        sequence_graph = SequenceGraph()
        sequences: list[Sequence] = []

        for pathway in project.sorted_pathways:
            if pathway.parent_id is None:
                continue

            action_node = action_nodes[pathway.id]
            parent_action_node = action_nodes[pathway.parent_id]
            sequence_graph.add_sequence(parent_action_node, action_node)
            sequences.append((parent_action_node.action, action_node.action))

        # Mostly copied from plot_pathway_map.py
        level_by_action = action_level_by_first_occurrence(sequences)

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)

        if pathway_map.nr_nodes() > 0:
            pathway_map.assign_tipping_points(tipping_points, verify=True)

        pathway_map.set_attribute("level_by_action", level_by_action)
        pathway_map.set_attribute("colour_by_action_name", action_colors)

        figure, axes = plt.subplots(layout="constrained")
        init_axes(axes)

        arguments: dict[str, Any] = {}
        arguments["colour_by_action_name"] = action_colors
        arguments["overlapping_lines_spread"] = 0.02
        arguments["tipping_point_overshoot"] = 0.2

        if for_export:
            arguments["x_label"] = f"{metric.name} ({metric.unit.symbol})"
            arguments["show_legend"] = True

        plot_classic_pathway_map(axes, pathway_map, arguments=arguments)

        return (figure, axes)
