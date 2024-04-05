Develop
=======

.. toctree::
   :maxdepth: 1

   API <../api/modules>
   Index <../genindex>
   Examples <example/index>


Development environment
-----------------------

If you want to help improve the software, the first thing you need to do is clone the Git
repository that contains the source code:

.. code-block:: bash

   cd ...  # Prefix of some location that should end up containing the repository clone
   # TODO Fix url once repository is moved to a shared location
   git clone ssh://git@some_server:some_port/some_organization/adaptation_pathways.git

The steps for setting up a development environment are as follows:

#. Create and activate a new virtual environment
#. Install all required Python and non-Python packages
#. Install :ref:`pre-commit hooks <sec-pre-commit>`
#. Verify everything works

In commands:

.. code-block:: bash

   cd adaptation_pathways  # The repository clone
   python3 -m venv env
   source env/bin/activate
   pip3 install --upgrade pip

   # Install software needed to help develop our software:
   pip3 install -r environment/configuration/requirements.txt -r environment/configuration/requirements-dev.txt

   # Install handy tools that will keep our code in good shape:
   pre-commit install
   # Note: commit .pre-commit-config.yaml if any hooks actually got updated
   pre-commit autoupdate

   source/script/ap_pathway_generator.py --help


The project contains code for generating :ref:`targets <sec-cmake>`, like documentation and the
installation package. Create a new directory for storing these. It is best to create this directory
outside of the source directory. CMake is used to generate build scripts that will do the actual
work. We use the Ninja build tool here, but you can use any build tool supported by CMake.

.. code-block:: bash

   # Assuming we are in the adaptation_pathways source directory...

   mkdir ../build
   cd ../build
   cmake -S ../adaptation_pathways -G Ninja

   # Execute the tests
   ninja test

   # Generate the documentation
   ninja documentation

   # Create the package
   ninja package

   # List all targets
   ninja -t targets


Create and test a package
-------------------------
Creating a package and inspecting its contents can be done as follows:

.. code-block:: bash

   # In build directory
   ninja
   ninja package
   tar -tf dist/adaptation_pathways-1.2.3.tar.gz
   unzip -l dist/adaptation_pathways-1.2.3-py3-none-any.whl

Creating a package (``ninja package``) results in a Wheel file in the ``dist`` directory in
the project's output directory. The next commands can be used to test the package.

.. code-block:: bash

   python3 -m venv ap_test
   source ap_test/bin/activate
   pip install --upgrade pip
   pip install -f dist adaptation_pathways
   adaptation_pathways --help

After testing the package, new versions of the package can be installed like this:

.. code-block:: bash

   pip install upgrade -f dist adaptation_pathways


Release a package
-----------------

.. warning::

   Double-check that all changes are committed.


Python package
~~~~~~~~~~~~~~

#. Create zip with Python Wheel package and the documentation, and verify the contents are OK:

   .. code-block:: bash

      # In build directory
      create_and_verify_release.py .

   .. warning::

      Do not release the package when this command fails.

   Output is stored in ``adaptation_pathways-1.2.3.zip``.

#. Copy the zip to a location users can find it.


Pathway generator
~~~~~~~~~~~~~~~~~

#. On all platforms the users care about, create a zip containing the pathway generator. This
   zip contains a directory with all requirements needed to use the software. It is portable:
   users can install multiple versions, anywhere they like.

   .. code-block:: bash

      # In build directory
      ninja installer_release

   Output is stored in ``pathway_generator-<system>-<version>.zip``

#. Copy the zip to a location users can find it.

.. note::

  On Windows, executing the pathway generator executable may fail because the virus scanner
  thinks it contains a virus. The virus scanner is wrong.


Wrap-up
~~~~~~~

#. Create and push a tag.

   .. code-block:: bash

      # In source directory
      git tag -a v1.2.3 -m"Release that adds cool features and solves all problems"
      git push origin v1.2.3

#. Bump the version number in these files:

   - ``CMakeLists.txt``
   - ``pyproject.toml``
   - ``source/package/adaptation_pathways/version.py``

#. Add a section for the upcoming version to the :ref:`changelog <sec-changelog>`: ``documentation/changelog.rst``.


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
