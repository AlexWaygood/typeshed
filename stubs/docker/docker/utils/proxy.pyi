from collections.abc import Sequence
from typing import TypedDict
from typing_extensions import NotRequired

class _ProxyConfigDict(TypedDict):
    http: NotRequired[str]
    https: NotRequired[str]
    ftpProxy: NotRequired[str]
    noProxy: NotRequired[str]

class _Environment(TypedDict):
    http_proxy: NotRequired[str]
    HTTP_PROXY: NotRequired[str]
    https_proxy: NotRequired[str]
    HTTPS_PROXY: NotRequired[str]
    ftp_proxy: NotRequired[str]
    FTP_PROXY: NotRequired[str]
    no_proxy: NotRequired[str]
    NO_PROXY: NotRequired[str]

class ProxyConfig(dict[str, str]):
    """
    Hold the client's proxy configuration
    """

    @property
    def http(self) -> str | None: ...
    @property
    def https(self) -> str | None: ...
    @property
    def ftp(self) -> str | None: ...
    @property
    def no_proxy(self) -> str | None: ...
    @staticmethod
    def from_dict(config: _ProxyConfigDict) -> ProxyConfig:
        """
        Instantiate a new ProxyConfig from a dictionary that represents a
        client configuration, as described in `the documentation`_.

        .. _the documentation:
            https://docs.docker.com/network/proxy/#configure-the-docker-client
        """

    def get_environment(self) -> _Environment:
        """
        Return a dictionary representing the environment variables used to
        set the proxy settings.
        """

    def inject_proxy_environment(self, environment: None | Sequence[str]) -> None | Sequence[str]:
        """
        Given a list of strings representing environment variables, prepend the
        environment variables corresponding to the proxy settings.
        """
