"""
Pathway map for an example
==========================
"""

from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import SequenceGraph, sequence_graph_to_pathway_map
from adaptation_pathways.io import text
from adaptation_pathways.plot import init_axes
from adaptation_pathways.plot import plot_default_pathway_map as plot


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

current    a[1]

current    b[1]
b[1]       a[2]
b[1]       c[2]
c[2]       b[2]
b[2]       a[3]
c[2]       a[4]
c[2]       d[3]
b[1]       d[2]

current    c[1]
c[1]       b[3]
b[3]       a[5]
c[1]       a[6]
c[1]       d[4]

current    d[1]
"""
    ),
    actions,
)
sequence_graph = SequenceGraph(sequences)
pathway_map = sequence_graph_to_pathway_map(sequence_graph)

colour_by_action_name = {
    action.name: colour for action, colour in colour_by_action.items()
}

pathway_map.set_attribute("colour_by_action_name", colour_by_action_name)

_, axes = plt.subplots(layout="constrained")
init_axes(axes)
plot(axes, pathway_map)
plt.show()
