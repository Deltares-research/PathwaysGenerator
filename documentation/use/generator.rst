Pathway Generator
=================
See also: :mod:`adaptation_pathways.cli.pathway_generator`

The package contains a GUI application called ``ap_pathway_generator``. It can be used to
interactively create pathways and save the results to a (binary) file.

.. note::

   The pathway generator is a proof of concept application. It proofs that the pathway plots
   can be made part of an easy to install desktop application, made with Python. It is not
   finished and not fool-proof yet. There are many things not working correctly or still missing.

Example for starting the application and initializing it with information from a text- or
binary-formatted dataset called ``my_pathways``.

.. code-block:: bash

   ap_pathway_generator my_pathways

For help about the usage of the command type ``ap_pathway_generator --help``.
