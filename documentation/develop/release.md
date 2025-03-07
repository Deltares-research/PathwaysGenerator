# Release a version

## Create and test a package
Creating a package and inspecting its contents can be done as follows:

```bash
# In build directory
ninja
ninja package
tar -tf dist/adaptation_pathways-1.2.3.tar.gz
unzip -l dist/adaptation_pathways-1.2.3-py3-none-any.whl
```

Creating a package (`ninja package`) results in a Wheel file in the `dist` directory in
the project's output directory. The next commands can be used to test the package.

```bash
python3 -m venv ap_test
source ap_test/bin/activate
pip install --upgrade pip
pip install -f dist adaptation_pathways
adaptation_pathways --help
```

After testing the package, new versions of the package can be installed like this:

```bash
pip install upgrade -f dist adaptation_pathways
```


## Release a package

```{warning}
Double-check that all changes are committed.
```


### Python package

1. Create zip with Python Wheel package and the documentation, and verify the contents are OK:

   ```bash
   # In build directory
   create_and_verify_release.py .
   ```

   ```{warning}
   Do not release the package when this command fails.
   ```

   Output is stored in `adaptation_pathways-1.2.3.zip`.

1. Copy the zip to a location users can find it.


### Pathway generator

1. On all platforms the users care about, create a zip containing the pathway generator. This zip contains a
   directory with all requirements needed to use the software. It is portable: users can install multiple
   versions, anywhere they like.

   ```bash
   # In build directory
   ninja installer_release
   ```

   Output is stored in `pathway_generator-<system>-<version>.zip`

1. Copy the zip to a location users can find it.

```{note}
On Windows, executing the pathway generator executable may fail because the virus scanner thinks it contains a
virus. The virus scanner is wrong.
```


### Wrap-up

1. Create and push a tag.

   ```bash
   # In source directory
   git tag -a v1.2.3 -m"Release that adds cool features and solves all problems"
   git push origin v1.2.3
   ```

1. Bump the version number in these files:

   - `CMakeLists.txt`
   - `pyproject.toml`
   - `source/package/adaptation_pathways/version.py`

1. Add a section for the upcoming version to the [changelog](#changelog): `documentation/changelog.md`.
