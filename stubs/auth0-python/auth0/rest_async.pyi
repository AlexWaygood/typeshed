from _typeshed import Incomplete

from auth0.types import RequestData

from .rest import RestClient

class AsyncRestClient(RestClient):
    """Provides simple methods for handling all RESTful api endpoints.

    Args:
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

    timeout: Incomplete
    def set_session(self, session) -> None:
        """Set Client Session to improve performance by reusing session.
        Session should be closed manually or within context manager.
        """

    async def get(self, url: str, params: dict[str, Incomplete] | None = None, headers: dict[str, str] | None = None): ...
    async def post(self, url: str, data: RequestData | None = None, headers: dict[str, str] | None = None): ...
    async def file_post(  # type: ignore[override] # Differs from supertype
        self, url: str, data: dict[str, Incomplete], files: dict[str, Incomplete]
    ): ...
    async def patch(self, url: str, data: RequestData | None = None): ...
    async def put(self, url: str, data: RequestData | None = None): ...
    async def delete(self, url: str, params: dict[str, Incomplete] | None = None, data: RequestData | None = None): ...

class RequestsResponse:
    status_code: int
    headers: Incomplete
    text: str
    def __init__(self, response, text: str) -> None: ...
