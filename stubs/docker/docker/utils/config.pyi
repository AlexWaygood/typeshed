from _typeshed import FileDescriptorOrPath
from logging import Logger
from typing import Final

DOCKER_CONFIG_FILENAME: Final[str]
LEGACY_DOCKER_CONFIG_FILENAME: Final[str]
log: Logger

def find_config_file(config_path: FileDescriptorOrPath | None = None) -> FileDescriptorOrPath | None: ...
def config_path_from_environment() -> str | None: ...
def home_dir() -> str:
    """
    Get the user's home directory, using the same logic as the Docker Engine
    client - use %USERPROFILE% on Windows, $HOME/getuid on POSIX.
    """

def load_general_config(config_path: FileDescriptorOrPath | None = None): ...
