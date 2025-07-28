"""
pygments.cmdline
~~~~~~~~~~~~~~~~

Command line interface.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

import argparse

def main_inner(parser, argns): ...

class HelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog, indent_increment: int = 2, max_help_position: int = 16, width=None) -> None: ...

def main(args=...):
    """
    Main command line entry point.
    """
