"""HTTP Client library"""

from email.message import Message
from http.client import HTTPResponse
from typing import Any, Final

class Response:
    """Holds the response from an API call."""

    def __init__(self, response: HTTPResponse) -> None:
        """
        :param response: The return value from a open call
                         on a urllib.build_opener()
        :type response:  urllib response object
        """

    @property
    def status_code(self) -> int:
        """
        :return: integer, status code of API call
        """

    @property
    def body(self) -> bytes:
        """
        :return: response from the API
        """

    @property
    def headers(self) -> Message:
        """
        :return: dict of response headers
        """

    @property
    def to_dict(self) -> dict[str, Any] | None:  # dict of response from API if body is not empty
        """
        :return: dict of response from the API
        """

class Client:
    """Quickly and easily access any REST or REST-like API."""

    methods: Final[set[str]]
    host: str
    request_headers: dict[str, str]
    append_slash: bool
    timeout: int
    def __init__(
        self,
        host: str,
        request_headers: dict[str, str] | None = None,
        version: int | None = None,
        url_path: list[str] | None = None,
        append_slash: bool = False,
        timeout: int | None = None,
    ) -> None:
        """
        :param host: Base URL for the api. (e.g. https://api.sendgrid.com)
        :type host:  string
        :param request_headers: A dictionary of the headers you want
                                applied on all calls
        :type request_headers: dictionary
        :param version: The version number of the API.
                        Subclass _build_versioned_url for custom behavior.
                        Or just pass the version as part of the URL
                        (e.g. client._("/v3"))
        :type version: integer
        :param url_path: A list of the url path segments
        :type url_path: list of strings
        """

    def _(self, name: str) -> Client:
        """Add variable values to the url.
           (e.g. /your/api/{variable_value}/call)
           Another example: if you have a Python reserved word, such as global,
           in your url, you must use this method.

        :param name: Name of the url segment
        :type name: string
        :return: Client object
        """

    def __getattr__(self, name: str) -> Client | Response:
        """Dynamically add method calls to the url, then call a method.
           (e.g. client.name.name.method())
           You can also add a version number by using .version(<int>)

        :param name: Name of the url segment or method call
        :type name: string or integer if name == version
        :return: mixed
        """
