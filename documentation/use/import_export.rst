.. _import_export:

Import and export
=================

The package contains two utilities for translating information about the pathways from text
formats to a binary format and back: ``ap_import`` and ``ap_export``.


Text format
-----------

Information about pathways can be stored in two text files, named ``<basename>-action.txt``
and ``<basename>-sequence.txt``. The ``<basename>`` part can be replaced by any name that makes
sense to you.

Comments are supported. A comment starts with a pound sign (``#``) and a space and can
occur anywhere in a file.

``<basename>-action.txt``
~~~~~~~~~~~~~~~~~~~~~~~~~
This file contains columns with information about the actions:

- name: string without spaces
- colour: Information about the RGBA values, in hexadecimal format

Example::

    current #ff4c566a
    a #ffbf616a
    b #ffd08770
    c #ffebcb8b

Actions can be defined in terms of other actions (action combinations). This may have an
influence on how such actions are visualized. The format for that is:
``action(other_action1 & other_action2)``. For example, in the previous example, an action
combination ``d`` could be added as follows::

    d(a & b) #ffa3be8c


``<basename>-sequence.txt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This file contains columns with information about the sequences of actions that together make
up pathways:

- from-action name: name of action from ``<basename>-action.txt``
- to-action name: name of action from ``<basename>-action.txt``
- tipping point: integer ≥ 0

Example::

    current     current 2030
    current     a       2040
    current     b       2050
    a           c       2060

To differentiate the same action in different pathways, action editions can be used. The format
for that is: ``action[edition]``. For example, in the previous example, action ``c`` can also
be used as a continuation of the sequence ``current b`` as follows::

    b           c[2]    2070


Import from text format to binary format
----------------------------------------
See also: :mod:`adaptation_pathways.cli.import_`, :mod:`adaptation_pathways.io`

Example for importing data from ``my_pathways-action.txt`` and ``my_pathways-sequence.txt`` to
``my_pathways.apw``:

.. code-block:: bash

   ap_import my_pathways my_pathways

For help about the usage of the command type ``ap_import --help``.


Export from binary format to text format
----------------------------------------
See also: :mod:`adaptation_pathways.cli.export`, :mod:`adaptation_pathways.io`

Example for exporting data from ``my_pathways.apw`` to ``my_pathways-action.txt`` and
``my_pathways-sequence.txt``:

.. code-block:: bash

   ap_export my_pathways my_pathways

For help about the usage of the command type ``ap_export --help``.
