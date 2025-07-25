from collections.abc import Callable, Iterator, MutableMapping
from typing import Any, NamedTuple

from jwcrypto.jwe import JWE
from jwcrypto.jws import JWS

def base64url_encode(payload: str | bytes) -> str: ...
def base64url_decode(payload: str) -> bytes: ...
def json_encode(string: str | bytes) -> str: ...

# The function returns json.loads which returns Any
def json_decode(string: str | bytes) -> Any: ...

class JWException(Exception): ...

class InvalidJWAAlgorithm(JWException):
    def __init__(self, message: str | None = None) -> None: ...

class InvalidCEKeyLength(JWException):
    """Invalid CEK Key Length.

    This exception is raised when a Content Encryption Key does not match
    the required length.
    """

    def __init__(self, expected: int, obtained: int) -> None: ...

class InvalidJWEOperation(JWException):
    """Invalid JWS Object.

    This exception is raised when a requested operation cannot
    be execute due to unsatisfied conditions.
    """

    def __init__(self, message: str | None = None, exception: BaseException | None = None) -> None: ...

class InvalidJWEKeyType(JWException):
    """Invalid JWE Key Type.

    This exception is raised when the provided JWK Key does not match
    the type required by the specified algorithm.
    """

    def __init__(self, expected: int, obtained: int) -> None: ...

class InvalidJWEKeyLength(JWException):
    """Invalid JWE Key Length.

    This exception is raised when the provided JWK Key does not match
    the length required by the specified algorithm.
    """

    def __init__(self, expected: int, obtained: int) -> None: ...

class InvalidJWSERegOperation(JWException):
    """Invalid JWSE Header Registry Operation.

    This exception is raised when there is an error in trying to add a JW
    Signature or Encryption header to the Registry.
    """

    def __init__(self, message: str | None = None, exception: BaseException | None = None) -> None: ...

class JWKeyNotFound(JWException):
    """The key needed to complete the operation was not found.

    This exception is raised when a JWKSet is used to perform
    some operation and the key required to successfully complete
    the operation is not found.
    """

    def __init__(self, message: str | None = None) -> None: ...

class JWSEHeaderParameter(NamedTuple):
    """Parameter(description, mustprotect, supported, check_fn)"""

    description: str
    mustprotect: bool
    supported: bool
    check_fn: Callable[[JWS | JWE], bool] | None

class JWSEHeaderRegistry(MutableMapping[str, JWSEHeaderParameter]):
    def __init__(self, init_registry: dict[str, JWSEHeaderParameter] | None = None) -> None: ...
    def check_header(self, h: str, value: JWS | JWE) -> bool: ...
    def __getitem__(self, key: str) -> JWSEHeaderParameter: ...
    def __iter__(self) -> Iterator[str]: ...
    def __delitem__(self, key: str) -> None: ...
    def __setitem__(self, h: str, jwse_header_param: JWSEHeaderParameter) -> None: ...
    def __len__(self) -> int: ...
