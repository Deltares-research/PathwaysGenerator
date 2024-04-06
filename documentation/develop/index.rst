Develop
=======

.. toctree::
   :maxdepth: 1

   Development environment <environment>
   Create a release <release>
   Use of Git <git>
   API <../api/modules>
   Index <../genindex>
   Examples <example/index>


Notes on software we use
------------------------


.. _sec-cmake:

CMake
~~~~~

Pure Python developers may not already be familiar with `CMake <https://cmake.org>`_. CMake
solves the problem of managing dependencies between input files (sources) and output files
(targets) in a platform independent way.

For example, documentation is automatically generated from the Python code, using Sphinx. With
CMake we can declare which commands are needed to do this.

CMake will generate project files that will eventually do whatever it takes to generate all
output targets, like the generated documentation. The project files generated can be any kind
you prefer, like GNU Makefile, Ninja, Microsoft Visual Studio, etc.

Software developers often have a preference for the contents of their software development
environment. They may like to use a certain operating system, integrated development environment,
editor, etc. The use of CMake helps to allow them to keep using their preferred environment.

If you need to learn more about CMake then the `Professional CMake
<https://crascit.com/professional-cmake/>`_ book is highly recommended.


.. _sec-pre-commit:

pre-commit
~~~~~~~~~~

When working with multiple people on a code-base, there have to be some rules in place to keep
the code in a good shape. There are many tools that can help enforce such rules. Development
environments can be configured in such a way that such tools are run while editing the code or
at least just before changes are committed to the repository. `Pre-commit
<https://pre-commit.com>`_ supports this latter scenario. When installed and configured, it
runs a set of tools on the changed source files and will only allow the commit to succeed if
none of the tools reports an error.

.. important::

   When helping to improve the software, it is essential that pre-commit is installed and
   configured before committing any changes to the repository.


Background information
----------------------

* `venv for creating virtual environments <https://docs.python.org/3/library/venv.html>`_
* `Sphinx documentation generator <https://www.sphinx-doc.org/en/master/>`_

* Build a package:

    * `Python Packaging User Guide <https://packaging.python.org/en/latest/>`_
    * `build packaging frontend <https://build.pypa.io/en/stable/>`_
    * `Hatch packaging backend <https://hatch.pypa.io/latest/>`_
    * `pip package installer <https://pip.pypa.io/en/stable/>`_

* Check and style the code:

    * `Black <https://black.readthedocs.io/en/stable/>`_
    * `Flake8 <https://flake8.pycqa.org/en/latest/>`_
    * `Mypy <https://mypy-lang.org/>`_
    * `Pylint <https://pylint.readthedocs.io/en/latest/>`_

* Packages used:

    * `NetworkX <https://networkx.org/documentation/stable/>`_
