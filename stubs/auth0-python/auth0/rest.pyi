from _typeshed import Incomplete
from collections.abc import Mapping
from typing import Final

import requests
from auth0.rest_async import RequestsResponse
from auth0.types import RequestData, TimeoutType

UNKNOWN_ERROR: Final[str]

class RestClientOptions:
    """Configuration object for RestClient. Used for configuring
            additional RestClient options, such as rate-limit
            retries.

    Args:
        telemetry (bool, optional): Enable or disable Telemetry
            (defaults to True)
        timeout (float or tuple, optional): Change the requests
            connect and read timeout. Pass a tuple to specify
            both values separately or a float to set both to it.
            (defaults to 5.0 for both)
        retries (integer): In the event an API request returns a
            429 response header (indicating rate-limit has been
            hit), the RestClient will retry the request this many
            times using an exponential backoff strategy, before
            raising a RateLimitError exception. 10 retries max.
            (defaults to 3)
    """

    telemetry: bool
    timeout: TimeoutType
    retries: int
    def __init__(self, telemetry: bool = True, timeout: TimeoutType = 5.0, retries: int = 3) -> None: ...

class RestClient:
    """Provides simple methods for handling all RESTful api endpoints.

    Args:
        jwt (str, optional): The JWT to be used with the RestClient.
        telemetry (bool, optional): Enable or disable Telemetry
            (defaults to True)
        timeout (float or tuple, optional): Change the requests
            connect and read timeout. Pass a tuple to specify
            both values separately or a float to set both to it.
            (defaults to 5.0 for both)
        options (RestClientOptions): Pass an instance of
            RestClientOptions to configure additional RestClient
            options, such as rate-limit retries. Overrides matching
            options passed to the constructor.
            (defaults to 3)
    """

    options: RestClientOptions
    jwt: str | None
    base_headers: dict[str, str]
    telemetry: bool
    timeout: TimeoutType
    def __init__(
        self, jwt: str | None, telemetry: bool = True, timeout: TimeoutType = 5.0, options: RestClientOptions | None = None
    ) -> None: ...
    def MAX_REQUEST_RETRIES(self) -> int: ...
    def MAX_REQUEST_RETRY_JITTER(self) -> int: ...
    def MAX_REQUEST_RETRY_DELAY(self) -> int: ...
    def MIN_REQUEST_RETRY_DELAY(self) -> int: ...
    def get(self, url: str, params: dict[str, Incomplete] | None = None, headers: dict[str, str] | None = None): ...
    def post(self, url: str, data: RequestData | None = None, headers: dict[str, str] | None = None): ...
    def file_post(self, url: str, data: RequestData | None = None, files: dict[str, Incomplete] | None = None): ...
    def patch(self, url: str, data: RequestData | None = None): ...
    def put(self, url: str, data: RequestData | None = None): ...
    def delete(self, url: str, params: dict[str, Incomplete] | None = None, data: RequestData | None = None): ...

class Response:
    def __init__(self, status_code: int, content, headers: Mapping[str, str]) -> None: ...
    def content(self): ...

class JsonResponse(Response):
    def __init__(self, response: requests.Response | RequestsResponse) -> None: ...

class PlainResponse(Response):
    def __init__(self, response: requests.Response | RequestsResponse) -> None: ...

class EmptyResponse(Response):
    def __init__(self, status_code: int) -> None: ...
