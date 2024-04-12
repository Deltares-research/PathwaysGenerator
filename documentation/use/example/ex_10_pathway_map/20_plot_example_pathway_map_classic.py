"""
Pathway map for an example
==========================
"""

from io import StringIO

import matplotlib.pyplot as plt

from adaptation_pathways.graph import SequenceGraph, sequence_graph_to_pathway_map
from adaptation_pathways.io import text
from adaptation_pathways.plot import (
    action_level_by_first_occurrence,
    init_axes,
    plot_classic_pathway_map,
)


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
current     current 2030
current     a       2040
a           e[1]    2090
current     b       2050
b           f[1]    2080
current     c       2060
c           f[2]    2080
current     d       2070
d           f[3]    2080
f[1]        e[2]    2090
f[2]        e[3]    2090
f[3]        e[4]    2090
"""
    ),
    actions,
)
sequence_graph = SequenceGraph(sequences)
pathway_map = sequence_graph_to_pathway_map(sequence_graph)

level_by_action = action_level_by_first_occurrence(sequences)
colour_by_action_name = {
    action.name: colour for action, colour in colour_by_action.items()
}

pathway_map.assign_tipping_points(tipping_point_by_action)
pathway_map.set_attribute("level_by_action", level_by_action)
pathway_map.set_attribute("colour_by_action_name", colour_by_action_name)

_, axes = plt.subplots(layout="constrained")
init_axes(axes)
plot_classic_pathway_map(axes, pathway_map)
plt.show()
