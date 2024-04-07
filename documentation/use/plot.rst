Plotting pathways
=================

.. toctree::
   :maxdepth: 1

   Examples <example/index>


The package contains two command-line applications. One is called ``ap_plot_graphs`` and can
be used to gain insight into various kinds of graphs used to store information about pathways,
and one is called ``ap_plot_pathway_map`` and can be used to visualize pathway maps in the
so-called :const:`CLASSIC <adaptation_pathways.plot.util.PathwayMapLayout.CLASSIC>` layout.


``ap_plot_graphs``
------------------
See also:
:mod:`adaptation_pathways.cli.plot_graphs`,
:class:`SequenceGraph <adaptation_pathways.graph.sequence_graph.SequenceGraph>`,
:class:`PathwayGraph <adaptation_pathways.graph.pathway_graph.PathwayGraph>`,
:class:`PathwayMap <adaptation_pathways.graph.pathway_map.PathwayMap>`

This command takes information about pathways as input, and outputs a plot of the sequence
graph, a plot of the pathway graph and a plot of the pathway map in :const:`DEFAULT
<adaptation_pathways.plot.util.PathwayMapLayout.DEFAULT>` layout.

Example for creating plots from ``my_pathways-action.txt`` and ``my_pathways-sequence.txt``
(or ``my_pathways.apw``) to ``./my_pathways-sequence_graph.pdf``,
``./my_pathways-pathway_graph.pdf``, and ``./my_pathways-pathway_map.pdf``:

.. code-block:: bash

   ap_plot_graphs my_pathways .

For help about the usage of the command type ``ap_plot_graphs --help``.


``ap_plot_pathway_map``
-----------------------
See also:
:mod:`adaptation_pathways.cli.plot_pathway_map`,
:class:`PathwayMap <adaptation_pathways.graph.pathway_map.PathwayMap>`

This command takes information about pathways as input, and outputs a single plot containing
the pathway map in :const:`CLASSIC <adaptation_pathways.plot.util.PathwayMapLayout.CLASSIC>`
layout.

Example for creating a plot from ``my_pathways-action.txt`` and ``my_pathways-sequence.txt``
(or ``my_pathways.apw``) to ``./my_pathways.pdf``:

.. code-block:: bash

   ap_plot_pathway_map my_pathways my_pathways.pdf

For help about the usage of the command type ``ap_plot_pathway_map --help``.
