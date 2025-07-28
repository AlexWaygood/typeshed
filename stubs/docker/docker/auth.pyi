from _typeshed import FileDescriptorOrPath, Incomplete, ReadableBuffer
from collections.abc import Mapping, MutableMapping
from logging import Logger
from typing import Final
from typing_extensions import Self

INDEX_NAME: Final[str]
INDEX_URL: Final[str]
TOKEN_USERNAME: Final[str]
log: Logger

def resolve_repository_name(repo_name: str) -> tuple[str, str]: ...
def resolve_index_name(index_name: str) -> str: ...
def get_config_header(client, registry) -> bytes | None: ...
def split_repo_name(repo_name: str) -> tuple[str, str]: ...
def get_credential_store(authconfig: AuthConfig | MutableMapping[str, Incomplete], registry: str | None): ...

class AuthConfig(dict[str, Incomplete]):
    def __init__(self, dct: MutableMapping[str, Incomplete], credstore_env=None) -> None: ...
    @classmethod
    def parse_auth(
        cls, entries: Mapping[str, dict[Incomplete, Incomplete]], raise_on_error: bool = False
    ) -> dict[str, Incomplete]:
        """
        Parses authentication entries

        Args:
          entries:        Dict of authentication entries.
          raise_on_error: If set to true, an invalid format will raise
                          InvalidConfigFile

        Returns:
          Authentication registry.
        """

    @classmethod
    def load_config(
        cls, config_path: FileDescriptorOrPath | None, config_dict: dict[str, Incomplete] | None, credstore_env=None
    ) -> Self:
        """
        Loads authentication data from a Docker configuration file in the given
        root directory or if config_path is passed use given path.
        Lookup priority:
            explicit config_path parameter > DOCKER_CONFIG environment
            variable > ~/.docker/config.json > ~/.dockercfg
        """

    @property
    def auths(self) -> dict[str, Incomplete]: ...
    @property
    def creds_store(self): ...
    @property
    def cred_helpers(self): ...
    @property
    def is_empty(self) -> bool: ...
    def resolve_authconfig(self, registry: str | None = None):
        """
        Returns the authentication data from the given auth configuration for a
        specific registry. As with the Docker client, legacy entries in the
        config with full URLs are stripped down to hostnames before checking
        for a match. Returns None if no match was found.
        """

    def get_credential_store(self, registry: str | None): ...
    def get_all_credentials(self): ...
    def add_auth(self, reg: str, data) -> None: ...

def resolve_authconfig(authconfig, registry: str | None = None, credstore_env=None): ...
def convert_to_hostname(url: str) -> str: ...
def decode_auth(auth: str | ReadableBuffer) -> tuple[str, str]: ...
def encode_header(auth) -> bytes: ...
def parse_auth(entries: Mapping[str, dict[Incomplete, Incomplete]], raise_on_error: bool = False):
    """
    Parses authentication entries

    Args:
      entries:        Dict of authentication entries.
      raise_on_error: If set to true, an invalid format will raise
                      InvalidConfigFile

    Returns:
      Authentication registry.
    """

def load_config(
    config_path: FileDescriptorOrPath | None = None, config_dict: dict[str, Incomplete] | None = None, credstore_env=None
) -> AuthConfig: ...
