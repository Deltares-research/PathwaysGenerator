Development environment
=======================

Clone repository
----------------

If you want to help improve the software, the first thing you need to do is clone the Git
repository that contains the source code:

.. code-block:: bash

   cd ...  # Prefix of some location that should end up containing the repository clone
   git clone git@github.com:Deltares-research/PathwaysGenerator.git

This assumes that you have write access to the main Git repository, which may not be the case. It
is good practice to contribute to a software project by performing the following steps:

#. Fork the repository you want to contribute to to your own Github organization
#. Clone the forked version of the main repository
#. Make changes in a branch
#. Push this branch to your fork of the main repository
#. Create a pull-request (PR)

Once finished creating the PR, someone with write access to the main repository (could be you
as well) can review the changes and eventually merge them.

* `Contributing to a project tutorial
  <https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project>`_


Setup environment
-----------------

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


Make some changes
-----------------

Here you can find an example workflow for submitting changes to the main repository. The commands
shown work in a Bash shell and use command-line Git. In case you use other software in your
development environment (e.g. Visual Studio Code) things will work differently, but the gist /
steps will be the same.

.. code-block:: bash

   # Assuming we are in the adaptation_pathways source directory...
   # Assuming the main branch is up to date with the main repository's main branch...

   # Assuming we will work on solving Github issue #5...
   # Create a new branch named after the issue number: Github issue number 5
   git checkout -b gh5

   # Make the changes..
   # ...

   # Push branch to your own fork
   git push -u origin gh5

In the Github page for your fork of the repository, there will now be button you can press
for creating the PR. Use the title of the Github issue that got solved for the title of the
PR. Add a comment similar to "Solves #5" to the PR. This will make sure that the issue gets
automatically close once the PR gets merged.

After making changes, verify locally that the unit tests still run and the code is still in
good shape. This will also be checked by the Github workflows setup for the repository. Doing it
locally results in a smoother process because it is more likely that your changes won't result
in workflows to fail.

.. code-block:: bash

   # Run unit tests
   ctest --test-dir build --output-on-failure

   # Alternatively, if you use Ninja
   ninja test

   # Alternatively, if you use GNU Make
   make test

   # Etc ;-)

If you have setup the pre-commit hooks correctly, various checks will be performed on the
changed files before they are actually committed.
