"""
This sub-package contains code related to I/O of information about adaptation pathways.
Two formats are supported: text and binary. The text format is useful to edit by hand, but
multiple files are needed to store all information, which may be inconvenient. The binary format
is useful because only a single file is used to store all information. Using the :ref:`import and
export command-line utilities <import_export>`, the formats can be translated into each other.
"""

from .dataset import read_dataset
