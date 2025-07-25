from .setopt import option_base

class saveopts(option_base):
    """Save command-line options to a file"""

    description: str
    def run(self) -> None: ...
