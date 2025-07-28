"""Procedure for parsing args, config, loading plugins."""

import argparse
from collections.abc import Sequence

from ..plugins import finder

def parse_args(argv: Sequence[str]) -> tuple[finder.Plugins, argparse.Namespace]:
    """Procedure for parsing args, config, loading plugins."""
