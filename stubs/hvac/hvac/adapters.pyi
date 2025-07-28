"""
HTTP Client Library Adapters

"""

from abc import ABCMeta, abstractmethod
from collections.abc import Mapping
from typing import Any, Generic, TypeVar
from typing_extensions import Self

from requests import Response, Session

_R = TypeVar("_R")

class Adapter(Generic[_R], metaclass=ABCMeta):
    """Abstract base class used when constructing adapters for use with the Client class."""

    @classmethod
    def from_adapter(cls, adapter: Adapter[_R]) -> Self:
        """Create a new adapter based on an existing Adapter instance.
        This can be used to create a new type of adapter that inherits the properties of an existing one.

        :param adapter: The existing Adapter instance.
        :type adapter: hvac.Adapters.Adapter
        """
    base_uri: str
    token: str | None
    namespace: str | None
    session: Session
    allow_redirects: bool
    ignore_exceptions: bool
    strict_http: bool
    request_header: bool
    def __init__(
        self,
        base_uri: str = "http://localhost:8200",
        token: str | None = None,
        cert: tuple[str, str] | None = None,
        verify: bool = True,
        timeout: int = 30,
        proxies: Mapping[str, str] | None = None,
        allow_redirects: bool = True,
        session: Session | None = None,
        namespace: str | None = None,
        ignore_exceptions: bool = False,
        strict_http: bool = False,
        request_header: bool = True,
    ) -> None:
        """Create a new request adapter instance.

        :param base_uri: Base URL for the Vault instance being addressed.
        :type base_uri: str
        :param token: Authentication token to include in requests sent to Vault.
        :type token: str
        :param cert: Certificates for use in requests sent to the Vault instance. This should be a tuple with the
            certificate and then key.
        :type cert: tuple
        :param verify: Either a boolean to indicate whether TLS verification should be performed when sending requests to Vault,
            or a string pointing at the CA bundle to use for verification. See http://docs.python-requests.org/en/master/user/advanced/#ssl-cert-verification.
        :type verify: Union[bool,str]
        :param timeout: The timeout value for requests sent to Vault.
        :type timeout: int
        :param proxies: Proxies to use when preforming requests.
            See: http://docs.python-requests.org/en/master/user/advanced/#proxies
        :type proxies: dict
        :param allow_redirects: Whether to follow redirects when sending requests to Vault.
        :type allow_redirects: bool
        :param session: Optional session object to use when performing request.
        :type session: request.Session
        :param namespace: Optional Vault Namespace.
        :type namespace: str
        :param ignore_exceptions: If True, _always_ return the response object for a given request. I.e., don't raise an exception
            based on response status code, etc.
        :type ignore_exceptions: bool
        :param strict_http: If True, use only standard HTTP verbs in request with additional params, otherwise process as is
        :type strict_http: bool
        :param request_header: If true, add the X-Vault-Request header to all requests to protect against SSRF vulnerabilities.
        :type request_header: bool
        """

    @staticmethod
    def urljoin(*args: object) -> str:
        """Joins given arguments into a url. Trailing and leading slashes are stripped for each argument.

        :param args: Multiple parts of a URL to be combined into one string.
        :type args: str | unicode
        :return: Full URL combining all provided arguments
        :rtype: str | unicode
        """

    def close(self) -> None:
        """Close the underlying Requests session."""

    def get(self, url: str, **kwargs: Any) -> _R:
        """Performs a GET request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :type url: str | unicode
        :param kwargs: Additional keyword arguments to include in the requests call.
        :type kwargs: dict
        :return: The response of the request.
        :rtype: requests.Response
        """

    def post(self, url: str, **kwargs: Any) -> _R:
        """Performs a POST request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :type url: str | unicode
        :param kwargs: Additional keyword arguments to include in the requests call.
        :type kwargs: dict
        :return: The response of the request.
        :rtype: requests.Response
        """

    def put(self, url: str, **kwargs: Any) -> _R:
        """Performs a PUT request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :type url: str | unicode
        :param kwargs: Additional keyword arguments to include in the requests call.
        :type kwargs: dict
        :return: The response of the request.
        :rtype: requests.Response
        """

    def delete(self, url: str, **kwargs: Any) -> _R:
        """Performs a DELETE request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :type url: str | unicode
        :param kwargs: Additional keyword arguments to include in the requests call.
        :type kwargs: dict
        :return: The response of the request.
        :rtype: requests.Response
        """

    def list(self, url: str, **kwargs: Any) -> _R:
        """Performs a LIST request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :type url: str | unicode
        :param kwargs: Additional keyword arguments to include in the requests call.
        :type kwargs: dict
        :return: The response of the request.
        :rtype: requests.Response
        """

    def head(self, url: str, **kwargs: Any) -> _R:
        """Performs a HEAD request.

        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :type url: str | unicode
        :param kwargs: Additional keyword arguments to include in the requests call.
        :type kwargs: dict
        :return: The response of the request.
        :rtype: requests.Response
        """

    def login(self, url: str, use_token: bool = True, **kwargs: Any) -> Response:
        """Perform a login request.

        Associated request is typically to a path prefixed with "/v1/auth") and optionally stores the client token sent
            in the resulting Vault response for use by the :py:meth:`hvac.adapters.Adapter` instance under the _adapter
            Client attribute.

        :param url: Path to send the authentication request to.
        :type url: str | unicode
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the the :py:meth:`hvac.adapters.Adapter` instance under the _adapter Client attribute.
        :type use_token: bool
        :param kwargs: Additional keyword arguments to include in the params sent with the request.
        :type kwargs: dict
        :return: The response of the auth request.
        :rtype: requests.Response
        """

    @abstractmethod
    def get_login_token(self, response: _R) -> str:
        """Extracts the client token from a login response.

        :param response: The response object returned by the login method.
        :return: A client token.
        :rtype: str
        """

    @abstractmethod
    def request(
        self, method, url: str, headers: Mapping[str, str] | None = None, raise_exception: bool = True, **kwargs: Any
    ) -> _R:
        """Main method for routing HTTP requests to the configured Vault base_uri. Intended to be implement by subclasses.

        :param method: HTTP method to use with the request. E.g., GET, POST, etc.
        :type method: str
        :param url: Partial URL path to send the request to. This will be joined to the end of the instance's base_uri
            attribute.
        :type url: str | unicode
        :param headers: Additional headers to include with the request.
        :type headers: dict
        :param kwargs: Additional keyword arguments to include in the requests call.
        :type kwargs: dict
        :param raise_exception: If True, raise an exception via utils.raise_for_error(). Set this parameter to False to
            bypass this functionality.
        :type raise_exception: bool
        :return: The response of the request.
        :rtype: requests.Response
        """

class _GenericRawAdapter(Adapter[_R]):
    def get_login_token(self, response: _R) -> str: ...
    def request(
        self, method: str, url: str, headers: Mapping[str, str] | None = None, raise_exception: bool = True, **kwargs: Any
    ) -> _R: ...

class RawAdapter(_GenericRawAdapter[Response]):
    """
    The RawAdapter adapter class.
    This adapter adds Vault-specific headers as required and optionally raises exceptions on errors,
    but always returns Response objects for requests.
    """

class JSONAdapter(_GenericRawAdapter[Response | dict[Any, Any]]):
    """
    The JSONAdapter adapter class.
    This adapter works just like the RawAdapter adapter except that HTTP 200 responses are returned as JSON dicts.
    All non-200 responses are returned as Response objects.
    """

    def get_login_token(self, response: Response | dict[Any, Any]) -> str:
        """Extracts the client token from a login response.

        :param response: The response object returned by the login method.
        :type response: dict | requests.Response
        :return: A client token.
        :rtype: str
        """

    def request(self, *args: Any, **kwargs: Any) -> Response | dict[Any, Any]:
        """Main method for routing HTTP requests to the configured Vault base_uri.

        :param args: Positional arguments to pass to RawAdapter.request.
        :type args: list
        :param kwargs: Keyword arguments to pass to RawAdapter.request.
        :type kwargs: dict
        :return: Dict on HTTP 200 with JSON body, otherwise the response object.
        :rtype: dict | requests.Response
        """

Request = RawAdapter
