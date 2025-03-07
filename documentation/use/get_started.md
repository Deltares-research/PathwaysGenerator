# Get started

Here, we assume that you want to get started using the `adaptation_pathways` Python package distributed as a
so-called Python Wheel.

The `adaptation_pathways` Python package can be used by performing these steps in turn:

1. Create and activate a new virtual environment. There are multiple options for this. Below
   we show how to setup a virtual environment using Python's built-in venv module and using Conda.
1. Install all required Python packages
1. Use the software
1. Remove the virtual environment

This procedure will leave no traces on your computer. If you intent to use the software regularly, you can
keep the virtual environment as is, and install any updated versions of the software later.


## Create a virtual environment

Python's built-in venv module and Conda (and others) are alternatives with which you can achieve the same
thing: create one or more virtual environments to install Python packages in. You don't need to use Python's
venv module if you work with Conda, and vice versa.

In the examples below, a virtual environment called ap_test is created. You can of course pick any other name
for the environment.


### Using venv

- [Tutorial](https://docs.python.org/3/tutorial/venv.html)
- [Documentation](https://docs.python.org/3/library/venv.html)

```bash
cd ... # prefix of some directory for storing virtual environment
python3 -m venv ap_test
# Use Scripts instead of bin if you use Windows
source ap_test/bin/activate
pip3 install --upgrade pip
```


### Using Conda

- [Using pip in a Conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#pip-in-env)

```bash
# Python version must be >= 3.9
conda create --name ap_test python=3.12
conda activate ap_test
```


## Install packages

The software is packaged as a Python wheel file. The pip command can be used to install it.

```bash
cd ... # prefix of dist directory containing package(s)
pip3 install -f dist adaptation_pathways
```


## Use software

Once the software is installed correctly, the following should work:

```bash
# Use an installed script
ap_plot_pathway_map --help

# Use the package
python3 -c "import adaptation_pathways as ap; print(ap.__version__)"
```


## Upgrade software

Installing an updated version of the software can be done using this command:

```bash
pip3 install upgrade -f dist adaptation_pathways
```

## Remove virtual environment

### Using venv

Just remove the ap_test directory containing the virtual environment.


### Using Conda

Use the Conda command to remove the virtual environment and all packages installed in it.

```bash
conda deactivate
conda env remote --name ap_test
```
