"""
This sub-package contains code related to plotting pathway maps
"""

from .classic import plot as plot_classic_pathway_map
from .colour import edge_colours as pathway_map_edge_colours
from .colour import edge_styles as pathway_map_edge_styles
from .colour import node_colours as pathway_map_node_colours
from .colour import node_styles as pathway_map_node_styles
from .default import plot as plot_default_pathway_map
from .plot import PathwayMapLayout, plot_pathway_map
