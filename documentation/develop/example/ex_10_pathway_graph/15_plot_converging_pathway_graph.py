"""
Pathway graph for converging pathways
=====================================
"""

from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import SequenceGraph, sequence_graph_to_pathway_graph
from adaptation_pathways.io import text
from adaptation_pathways.plot import init_axes
from adaptation_pathways.plot import plot_default_pathway_graph as plot


actions, colour_by_action = text.read_actions(
    StringIO(
        """
current #ff4c566a
a #ffbf616a
b #ffd08770
c #ffebcb8b
d #ffa3be8c
"""
    )
)
sequences, tipping_point_by_action = text.read_sequences(
    StringIO(
        """
current[1] current
current a
current b
current c
a d[1]
b d[2]
c d[3]
"""
    ),
    actions,
)
sequence_graph = SequenceGraph(sequences)
pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)

colour_by_action_name = {
    action.name: colour for action, colour in colour_by_action.items()
}

pathway_graph.set_attribute("colour_by_action_name", colour_by_action_name)

_, axes = plt.subplots(layout="constrained")
init_axes(axes)
plot(axes, pathway_graph)
plt.show()
