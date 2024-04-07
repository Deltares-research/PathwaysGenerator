"""
Top-level package containing all code related to the Adaptation Pathways

All ``__init__.py`` files in this and the sub-packages are kept as empty as possible. This is
intentional, because the public API is still not stable. In general, to use functionality
from a package, developers must explicitly include the module containing the functionality. This
results in more import statements than necessary, but once the public API emerges this can
be remedied by letting the package's ``__init__.py`` import certain modules automatically.
"""

from .version import __version__
