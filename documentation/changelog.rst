.. _sec-changelog:

Changelog
=========
Description of of all notable changes made per version.


0.0.9
-----
- Support moving sequences in the sequences table of the pathway generator.
- Support writing and reading information about pathways to a binary file.
- Support import / export between text and binary dataset formats. See ``ap_import`` and
  ``ap_export`` commands.
- Visualize combinations of actions by dashed lines
- Added documentations (manuals and API)
- Moved repository to new location: https://github.com/Deltares-research/PathwaysGenerator
- Configured continuous integration. Every time we make changes, the source code is checked
  (style and functionality). https://github.com/Deltares-research/PathwaysGenerator/actions


0.0.8
-----
- Various improvements to the ``ap_pathway_generator`` command:
    - Define actions and assign colours to them
    - Define sequences
    - Visualize sequences graph
    - Visualize pathway graph
    - Visualize pathway map (default layout, without taking tipping points into account)


0.0.7
-----
- Ordering of actions in a pathway map (classic layout) is now based on the ordering of actions
  in the sequences file.
- Added custom pathway map plotting function for drawing pathway maps in the classic layout. Your
  can try it out using the ``ap_plot_pathway_map`` command.


0.0.6
-----
- Added support for specifying action editions: the same action can occur at different horizontal
  locations (at different periods in time or at ranges of conditions) in a pathway map. To make
  this possible, such actions must be differentiated from each other. This can now be done using
  editions, which are just integral values. Each action has one. When not specified, the edition
  of an action is zero. Example::

    # Action a occurs twice, but they are different editions
    current a[1]
    current b
    b a[2]


0.0.5
-----
- Added ``ap_plot_pathway_map`` command. See ``ap_plot_pathway_map --help`` for more information.
- Added support for specifying combinations of actions in the file containing sequences. Example::

    current a
    current b
    current c
    # Action a continues, but is combined with the new action e
    a d(a & e)
