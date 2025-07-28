"""Functions for constructing the requested report plugin."""

import argparse
from logging import Logger

from ..formatting.base import BaseFormatter
from .finder import LoadedPlugin

LOG: Logger

def make(reporters: dict[str, LoadedPlugin], options: argparse.Namespace) -> BaseFormatter:
    """Make the formatter from the requested user options.

    - if :option:`flake8 --quiet` is specified, return the ``quiet-filename``
      formatter.
    - if :option:`flake8 --quiet` is specified at least twice, return the
      ``quiet-nothing`` formatter.
    - otherwise attempt to return the formatter by name.
    - failing that, assume it is a format string and return the ``default``
      formatter.
    """
