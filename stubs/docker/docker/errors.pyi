from _typeshed import Incomplete
from collections.abc import Iterator, Mapping
from typing import NoReturn

from docker.models.containers import Container
from requests import HTTPError, Response

class DockerException(Exception):
    """
    A base class from which all other exceptions inherit.

    If you want to catch all errors that the Docker SDK might raise,
    catch this base exception.
    """

def create_api_error_from_http_exception(e: HTTPError) -> NoReturn:
    """
    Create a suitable APIError from requests.exceptions.HTTPError.
    """

class APIError(HTTPError, DockerException):
    """
    An HTTP error from the API.
    """

    response: Response | None
    explanation: str | None
    def __init__(self, message: str, response: Response | None = None, explanation: str | None = None) -> None: ...
    @property
    def status_code(self) -> int | None: ...
    def is_error(self) -> bool: ...
    def is_client_error(self) -> bool: ...
    def is_server_error(self) -> bool: ...

class NotFound(APIError): ...
class ImageNotFound(NotFound): ...
class InvalidVersion(DockerException): ...
class InvalidRepository(DockerException): ...
class InvalidConfigFile(DockerException): ...
class InvalidArgument(DockerException): ...
class DeprecatedMethod(DockerException): ...

class TLSParameterError(DockerException):
    msg: str
    def __init__(self, msg: str) -> None: ...

class NullResource(DockerException, ValueError): ...

class ContainerError(DockerException):
    """
    Represents a container that has exited with a non-zero exit code.
    """

    container: Container
    exit_status: Incomplete
    command: Incomplete
    image: Incomplete
    stderr: str | None
    def __init__(self, container: Container, exit_status, command, image, stderr: str | None) -> None: ...

class StreamParseError(RuntimeError):
    msg: str
    def __init__(self, reason: str) -> None: ...

class BuildError(DockerException):
    msg: str
    build_log: Iterator[dict[str, str]]
    def __init__(self, reason: str, build_log: Iterator[dict[str, str]]) -> None: ...

class ImageLoadError(DockerException): ...

def create_unexpected_kwargs_error(name, kwargs: Mapping[str, Incomplete]) -> NoReturn: ...

class MissingContextParameter(DockerException):
    param: str
    def __init__(self, param: str) -> None: ...

class ContextAlreadyExists(DockerException):
    name: str
    def __init__(self, name: str) -> None: ...

class ContextException(DockerException):
    msg: str
    def __init__(self, msg: str) -> None: ...

class ContextNotFound(DockerException):
    name: str
    def __init__(self, name: str) -> None: ...
