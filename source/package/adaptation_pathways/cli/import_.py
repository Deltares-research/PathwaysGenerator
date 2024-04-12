import os.path
import sys
from pathlib import Path

import docopt

from ..io import binary, text
from ..version import __version__ as version
from .main import main_function


@main_function
def import_(basename_pathname: str, dataset_pathname: str) -> int:

    actions, sequences, tipping_point_by_action, colour_by_action = text.read_dataset(
        basename_pathname
    )

    binary.write_dataset(
        actions,
        sequences,
        tipping_point_by_action,
        colour_by_action,
        Path(dataset_pathname),
    )

    return 0


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Import text files to dataset

Usage:
    {command} <basename> <dataset>

Arguments:
    basename           Name, without postfix and extension of group of files
                       to import from
    dataset            Pathname of dataset to import to. If the dataset
                       already exists, it will be overwritten.

Options:
    -h --help          Show this screen and exit
    --version          Show version and exit

Example:
    {command} serial serial.apw

This example imports information from the following files:
- serial-action.txt → Contains information about each action (required)
- serial-sequence.txt → Contains the sequences that make up pathways
  (required)
- serial-tipping_point.txt → Contains tipping points for each action edition
  (optional)

Information about how information in these file should be formatted can be
found in the documentation.
"""
    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=version)
    basename_pathname = arguments["<basename>"]  # type: ignore
    dataset_pathname = arguments["<dataset>"]  # type: ignore

    return import_(basename_pathname, dataset_pathname)
