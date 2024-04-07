import os.path
import sys

import docopt

from ..desktop.application import application
from ..version import __version__


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Generate adaptation pathways

Usage:
    {command} [<basename>]
    {command} -h | --help
    {command} --version

Options:
    basename           Either, the name without postfix and extension of text
                       file(s) to read information from, or the name of a
                       binary file to read information from.
    -h --help          Show this screen and exit
    --version          Show version and exit
"""
    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=__version__)
    basename_pathname = (
        arguments["<basename>"] if arguments["<basename>"] is not None else ""  # type: ignore
    )
    status = application(basename_pathname)

    return status
