"""Generic command line interface for the `docutils` package.

See also
https://docs.python.org/3/library/__main__.html#main-py-in-python-packages
"""

from typing import ClassVar

import docutils

class CliSettingsSpec(docutils.SettingsSpec):
    """Runtime settings & command-line options for the generic CLI.

    Configurable reader, parser, and writer components.

    The "--writer" default will change to 'html' in Docutils 2.0
    when 'html' becomes an alias for the current value 'html5'.
    """

    config_section: ClassVar[str]
    config_section_dependencies: ClassVar[tuple[str, ...]]

def main() -> None:
    """Generic command line interface for the Docutils Publisher."""
