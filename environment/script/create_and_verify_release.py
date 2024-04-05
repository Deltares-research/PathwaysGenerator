#!/usr/bin/env python3
import os.path
import shlex
import shutil
import subprocess
import sys
import venv
from pathlib import Path
from zipfile import ZipFile

import docopt

import adaptation_pathways as ap
from adaptation_pathways.cli.main import main_function


def verify_build_directory(build_directory_path: Path) -> None:
    assert build_directory_path.exists(), build_directory_path
    assert build_directory_path.is_dir(), build_directory_path
    assert (
        len(list(build_directory_path.glob("CMakeCache.txt"))) == 1
    ), f"{build_directory_path} is not a CMake binary directory"


def create_release(build_directory_path: Path) -> Path:
    release_zip_path = build_directory_path.joinpath(
        f"adaptation_pathways-{ap.__version__}.zip"
    )
    assert (
        not release_zip_path.exists()
    ), f"Release zip {release_zip_path} already exists. Remove it first."

    # Command for generating the release zip containing the documentation and the package wheel
    command = f"cmake --build {build_directory_path} --target release"
    subprocess.run(shlex.split(command), check=True)

    assert release_zip_path.exists()

    return release_zip_path


def verify_no_unnecessary_contents(release_directory_path: Path) -> None:
    """
    Verify that the release does not contain files and directories that it should not contain
    """
    package_directory_path = release_directory_path.joinpath(
        "venv",
        "lib",
        f"python{sys.version_info.major}.{sys.version_info.minor}",
        "site-packages",
        "adaptation_pathways",
    )
    documentation_directory_path = release_directory_path.joinpath("documentation")

    unnecessary_filename_patterns = [
        "CMakeLists.txt",
    ]

    for directory_path in [package_directory_path, documentation_directory_path]:
        assert directory_path.exists(), directory_path

        for pattern in unnecessary_filename_patterns:
            pathnames = list(directory_path.glob(f"**/{pattern}"))
            assert len(pathnames) == 0, pathnames


def verify_wheel(release_directory_path: Path) -> None:
    dist_directory_path = release_directory_path.joinpath("dist")
    assert dist_directory_path.exists()

    venv_directory_path = release_directory_path.joinpath("venv")
    assert not venv_directory_path.exists()

    venv.create(venv_directory_path, with_pip=True, upgrade_deps=True)
    assert venv_directory_path.exists()

    commands = [
        "set -e",  # Stop script when first command fails
        f"cd {release_directory_path}",
        "source venv/bin/activate",
        "pip3 install -f dist adaptation_pathways --quiet",
        "ap_plot_graphs --version",
        "ap_plot_pathway_map --version",
        "ap_pathway_generator --version",
        'python3 -c "'
        "import adaptation_pathways as ap;"
        f'assert ap.__version__ == \\"{ap.__version__}\\";'
        '"',
    ]
    subprocess.run(";".join(commands), shell=True, executable="/bin/bash", check=True)


def verify_documentation(release_directory_path: Path) -> None:
    html_directory_path = release_directory_path.joinpath("documentation", "html")
    assert html_directory_path.exists()

    index_html = html_directory_path.joinpath("index.html")

    assert index_html.exists()

    command = f"linkchecker {index_html}"

    subprocess.run(shlex.split(command), check=True)


def verify_release_directory(release_directory_path: Path) -> None:
    assert release_directory_path.exists()

    verify_wheel(release_directory_path)
    verify_documentation(release_directory_path)
    verify_no_unnecessary_contents(release_directory_path)


def verify_release(release_zip_path: Path) -> None:
    release_directory_path = Path(f"adaptation_pathways-{ap.__version__}")

    with ZipFile(release_zip_path) as release_zip:
        info = release_zip.getinfo(f"{release_directory_path}/")
        assert info.is_dir()
        release_zip.extractall()
        verify_release_directory(release_directory_path)
        shutil.rmtree(release_directory_path)


def create_and_verify_release(build_directory_path: Path) -> Path:
    verify_build_directory(build_directory_path)
    release_zip_path = create_release(build_directory_path)
    verify_release(release_zip_path)

    return release_zip_path


@main_function
def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Create a release and verify the contents seem OK

Usage:
    {command} <build_directory>

Arguments:
    build_directory  Pathname of project's build directory

Options:
    -h --help        Show this screen and exit
    --version        Show version and exit
"""
    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=ap.__version__)
    build_directory_path = Path(arguments["<build_directory>"])  # type: ignore

    release_zip_path = create_and_verify_release(build_directory_path)

    print(f"\nPackage {release_zip_path} is ready to be released!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
