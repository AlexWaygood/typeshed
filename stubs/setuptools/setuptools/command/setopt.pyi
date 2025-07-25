from _typeshed import Incomplete
from abc import abstractmethod
from typing import ClassVar

from .. import Command

__all__ = ["config_file", "edit_config", "option_base", "setopt"]

def config_file(kind: str = "local"):
    """Get the filename of the distutils, local, global, or per-user config

    `kind` must be one of "local", "global", or "user"
    """

def edit_config(filename, settings, dry_run: bool = False) -> None:
    """Edit a configuration file to include `settings`

    `settings` is a dictionary of dictionaries or ``None`` values, keyed by
    command/section name.  A ``None`` value means to delete the entire section,
    while a dictionary lists settings to be changed or deleted in that section.
    A setting of ``None`` means to delete that setting.
    """

class option_base(Command):
    """Abstract base class for commands that mess with config files"""

    user_options: ClassVar[list[tuple[str, str, str]]]
    boolean_options: ClassVar[list[str]]
    global_config: Incomplete
    user_config: Incomplete
    filename: Incomplete
    def initialize_options(self) -> None: ...
    def finalize_options(self) -> None: ...
    @abstractmethod
    def run(self) -> None:
        """
        Execute the actions intended by the command.
        (Side effects **SHOULD** only take place when :meth:`run` is executed,
        for example, creating new files or writing to the terminal output).
        """

class setopt(option_base):
    """Save command-line options to a file"""

    description: str
    user_options: ClassVar[list[tuple[str, str, str]]]
    boolean_options: ClassVar[list[str]]
    command: Incomplete
    option: Incomplete
    set_value: Incomplete
    remove: Incomplete
    def initialize_options(self) -> None: ...
    def finalize_options(self) -> None: ...
    def run(self) -> None: ...
