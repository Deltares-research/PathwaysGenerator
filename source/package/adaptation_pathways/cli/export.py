import os.path
import sys
from pathlib import Path

import docopt

from ..io import binary, text
from ..version import __version__ as version
from .main import main_function


@main_function
def export(dataset_pathname: str, basename_pathname: str) -> int:

    actions, sequences, tipping_point_by_action, colour_by_action = binary.read_dataset(
        Path(dataset_pathname)
    )

    text.write_dataset(
        actions, sequences, tipping_point_by_action, colour_by_action, basename_pathname
    )

    return 0


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Import text files to dataset

Usage:
    {command} <dataset> <basename>

Arguments:
    dataset            Pathname of dataset to export from
    basename           Name, without postfix and extension of group of files
                       to export to. Any existing output files will be
                       overwritten.

Options:
    -h --help          Show this screen and exit
    --version          Show version and exit

Example:
    {command} serial.apw serial

This example exports information to the following files:
- serial-action.txt → Contains information about each action (required)
- serial-sequence.txt → Contains the sequences that make up pathways
  (required)
- serial-tipping_point.txt → Contains tipping points for each action edition
  (optional)
"""
    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=version)
    dataset_pathname = arguments["<dataset>"]  # type: ignore
    basename_pathname = arguments["<basename>"]  # type: ignore

    return export(dataset_pathname, basename_pathname)
