from abc import ABC
from dataclasses import dataclass
from typing import Any
from typing_extensions import Self

from .common import Request, RequestHandler

@dataclass(order=True, frozen=True)
class ImpersonateTarget:
    """
    A target for browser impersonation.

    Parameters:
    @param client: the client to impersonate
    @param version: the client version to impersonate
    @param os: the client OS to impersonate
    @param os_version: the client OS version to impersonate

    Note: None is used to indicate to match any.

    """

    client: str | None = ...
    version: str | None = ...
    os: str | None = ...
    os_version: str | None = ...

    def __post_init__(self) -> None: ...
    def __contains__(self, target: Self) -> bool: ...
    @classmethod
    def from_str(cls, target: str) -> Self: ...

class ImpersonateRequestHandler(RequestHandler, ABC):
    """
    Base class for request handlers that support browser impersonation.

    This provides a method for checking the validity of the impersonate extension,
    which can be used in _check_extensions.

    Impersonate targets consist of a client, version, os and os_ver.
    See the ImpersonateTarget class for more details.

    The following may be defined:
     - `_SUPPORTED_IMPERSONATE_TARGET_MAP`: a dict mapping supported targets to custom object.
                Any Request with an impersonate target not in this list will raise an UnsupportedRequest.
                Set to None to disable this check.
                Note: Entries are in order of preference

    Parameters:
    @param impersonate: the default impersonate target to use for requests.
                        Set to None to disable impersonation.
    """

    _SUPPORTED_IMPERSONATE_TARGET_MAP: dict[ImpersonateTarget, Any] = ...  # Copied from source.

    def __init__(
        self,
        *,
        impersonate: ImpersonateTarget | None = None,
        # All keyword arguments are ignored (passed to RequestHandler as **kwargs but RequestHandler.__init__() has **_ and does
        # not use it).
        **kwargs: Any,
    ) -> None: ...
    @property
    def supported_targets(cls) -> tuple[ImpersonateTarget, ...]: ...
    def is_supported_target(self, target: ImpersonateTarget) -> bool: ...

def impersonate_preference(rh: RequestHandler, request: Request) -> int: ...
