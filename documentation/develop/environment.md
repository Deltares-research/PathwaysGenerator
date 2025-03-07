# Development environment

## Notes on software we use

(sec-cmake)=

### CMake

Pure Python developers may not already be familiar with [CMake](https://cmake.org). CMake solves the problem
of managing dependencies between input files (sources) and output files (targets) in a platform independent
way.

For example, documentation is automatically generated from the Python code, using Sphinx. With CMake we can
declare which commands are needed to do this.

CMake will generate project files that will eventually do whatever it takes to generate all output targets,
like the generated documentation. The project files generated can be any kind you prefer, like GNU Makefile,
Ninja, Microsoft Visual Studio, etc.

Software developers often have a preference for the contents of their software development environment. They
may like to use a certain operating system, integrated development environment, editor, etc. The use of CMake
helps to allow them to keep using their preferred environment.

If you need to learn more about CMake then the [Professional CMake
book](https://crascit.com/professional-cmake/) is highly recommended.


(sec-pre-commit)=

### pre-commit

When working with multiple people on a code-base, there have to be some rules in place to keep the code in a
good shape. There are many tools that can help enforce such rules. Development environments can be configured
in such a way that such tools are run while editing the code or at least just before changes are committed to
the repository. [Pre-commit](https://pre-commit.com) supports this latter scenario. When installed and
configured, it runs a set of tools on the changed source files and will only allow the commit to succeed if
none of the tools reports an error.

```{important}
When helping to improve the software, it is essential that pre-commit is installed and configured before
committing any changes to the repository.
```


## Background information

- [venv for creating virtual environments](https://docs.python.org/3/library/venv.html)
- [Sphinx documentation generator](https://www.sphinx-doc.org/en/master/)

- Build a package:

    - [Python Packaging User Guide](https://packaging.python.org/en/latest/)
    - [build packaging frontend](https://build.pypa.io/en/stable/)
    - [Hatch packaging backend](https://hatch.pypa.io/latest/)
    - [pip package installer](https://pip.pypa.io/en/stable/)

- Check and style the code:

    - [Black](https://black.readthedocs.io/en/stable/)
    - [Flake8](https://flake8.pycqa.org/en/latest/)
    - [Mypy](https://mypy-lang.org/)
    - [Pylint](https://pylint.readthedocs.io/en/latest/)

- Packages used:

    - [NetworkX](https://networkx.org/documentation/stable/)


## Clone repository

If you want to help improve the software, the first thing you need to do is clone the Git repository that
contains the source code:

```bash
cd ...  # Prefix of some location that should end up containing the repository clone
git clone git@github.com:Deltares-research/PathwaysGenerator.git
```

This assumes that you have write access to the main Git repository, which may not be the case. It is good
practice to contribute to a software project by performing the following steps:

1. Fork the repository you want to contribute to to your own Github organization
1. Clone the forked version of the main repository
1. Make changes in a branch
1. Push this branch to your fork of the main repository
1. Create a pull-request (PR)

Once finished creating the PR, someone with write access to the main repository (could be you as well) can
review the changes and eventually merge them.

- [Contributing to a project tutorial](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project)


## Setup environment

The steps for setting up a development environment are as follows:

1. Create and activate a new virtual environment
1. Install all required Python and non-Python packages
1. Install [pre-commit hooks](#sec-pre-commit)
1. Verify everything works

In commands:

```bash
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

source/script/ap_plot_pathway_map.py --help
```

The project contains code for generating [targets](#sec-cmake), like documentation and the installation
package. Create a new directory for storing these. It is best to create this directory outside of the source
directory. CMake is used to generate build scripts that will do the actual work. We use the Ninja build tool
here, but you can use any build tool supported by CMake.

```bash
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
```


## Make some changes

Here you can find an example workflow for submitting changes to the main repository. The commands shown work
in a Bash shell and use command-line Git. In case you use other software in your development environment (e.g.
Visual Studio Code) things will work differently, but the gist / steps will be the same.

```bash
# Assuming we are in the adaptation_pathways source directory...
# Assuming the main branch is up to date with the main repository's main branch...

# Assuming we will work on solving Github issue #5...
# Create a new branch named after the issue number: Github issue number 5
git checkout -b gh5

# Make the changes..
# ...

# Push branch to your own fork
git push -u origin gh5
```

In the Github page for your fork of the repository, there will now be button you can press for creating the
PR. Use the title of the Github issue that got solved for the title of the PR. Add a comment similar to
"Solves #5" to the PR. This will make sure that the issue gets automatically close once the PR gets merged.

After making changes, verify locally that the unit tests still run and the code is still in good shape. This
will also be checked by the Github workflows setup for the repository. Doing it locally results in a smoother
process because it is more likely that your changes won't result in workflows to fail.

```bash
# Run unit tests
ctest --test-dir build --output-on-failure

# Alternatively, if you use Ninja
ninja test

# Alternatively, if you use GNU Make
make test

# Etc ;-)
```

If you have setup the pre-commit hooks correctly, various checks will be performed on the changed files before
they are actually committed.
