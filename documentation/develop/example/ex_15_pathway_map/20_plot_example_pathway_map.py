"""
Pathway map for an example
==========================
"""

from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import SequenceGraph, sequence_graph_to_pathway_map
from adaptation_pathways.io import text
from adaptation_pathways.plot import init_axes, plot_default_pathway_map


actions, colour_by_action = text.read_actions(
    StringIO(
        """
current #ff4c566a
a #ffbf616a
b #ffd08770
c #ffebcb8b
d #ffa3be8c
e #ffb48ead
f #ff5e81ac
"""
    )
)
sequences, tipping_point_by_action = text.read_sequences(
    StringIO(
        """
current[1] current
current    a
a          e[1]
current    b
b          f[1]
current    c
c          f[2]
current    d
d          f[3]
f[1]       e[2]
f[2]       e[3]
f[3]       e[4]
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
plot_default_pathway_map(axes, pathway_map)
plt.show()
