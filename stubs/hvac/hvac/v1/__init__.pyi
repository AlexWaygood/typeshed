from typing import Any, Literal, overload

from hvac.adapters import Adapter
from hvac.api import AuthMethods, SystemBackend
from hvac.api.secrets_engines import SecretsEngines
from requests import Session
from requests.models import Response

has_hcl_parser: bool

class Client:
    """The hvac Client class for HashiCorp's Vault."""

    def __init__(
        self,
        url: str | None = None,
        token: str | None = None,
        cert: tuple[str, str] | None = None,
        verify: bool | str | None = None,
        timeout: int = 30,
        proxies: dict[str, str] | None = None,
        allow_redirects: bool = True,
        session: Session | None = None,
        adapter: type[Adapter[Any]] = ...,
        namespace: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Creates a new hvac client instance.

        :param url: Base URL for the Vault instance being addressed.
        :type url: str
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
        :param proxies: Proxies to use when performing requests.
            See: http://docs.python-requests.org/en/master/user/advanced/#proxies
        :type proxies: dict
        :param allow_redirects: Whether to follow redirects when sending requests to Vault.
        :type allow_redirects: bool
        :param session: Optional session object to use when performing request.
        :type session: request.Session
        :param adapter: Optional class to be used for performing requests. If none is provided, defaults to
            hvac.adapters.JSONRequest.
        :type adapter: hvac.adapters.Adapter
        :param kwargs: Additional parameters to pass to the adapter constructor.
        :type kwargs: dict
        :param namespace: Optional Vault Namespace.
        :type namespace: str
        """

    def __getattr__(self, name: str) -> Any: ...
    @property
    def adapter(self) -> Adapter[Any]:
        """Adapter for all client's connections."""

    @adapter.setter
    def adapter(self, adapter: Adapter[Any]) -> None: ...
    @property
    def url(self) -> str: ...
    @url.setter
    def url(self, url: str) -> None: ...
    @property
    def token(self) -> str: ...
    @token.setter
    def token(self, token: str) -> None: ...
    @property
    def session(self) -> Session: ...
    @session.setter
    def session(self, session: Session) -> None: ...
    @property
    def allow_redirects(self) -> bool: ...
    @allow_redirects.setter
    def allow_redirects(self, allow_redirects: bool) -> None: ...
    @property
    def auth(self) -> AuthMethods:
        """Accessor for the Client instance's auth methods. Provided via the :py:class:`hvac.api.AuthMethods` class.
        :return: This Client instance's associated Auth instance.
        :rtype: hvac.api.AuthMethods
        """

    @property
    def secrets(self) -> SecretsEngines:
        """Accessor for the Client instance's secrets engines. Provided via the :py:class:`hvac.api.SecretsEngines` class.

        :return: This Client instance's associated SecretsEngines instance.
        :rtype: hvac.api.SecretsEngines
        """

    @property
    def sys(self) -> SystemBackend:
        """Accessor for the Client instance's system backend methods.
        Provided via the :py:class:`hvac.api.SystemBackend` class.

        :return: This Client instance's associated SystemBackend instance.
        :rtype: hvac.api.SystemBackend
        """

    @property
    def generate_root_status(self) -> dict[str, Any] | Response: ...
    @property
    def key_status(self) -> dict[str, Any] | Response:
        """GET /sys/key-status

        :return: Information about the current encryption key used by Vault.
        :rtype: dict
        """

    @property
    def rekey_status(self) -> dict[str, Any] | Response: ...
    @property
    def ha_status(self) -> dict[str, Any] | Response:
        """Read the high availability status and current leader instance of Vault.

        :return: The JSON response returned by read_leader_status()
        :rtype: dict
        """

    @property
    def seal_status(self) -> dict[str, Any] | Response:
        """Read the seal status of the Vault.

        This is an unauthenticated endpoint.

        Supported methods:
            GET: /sys/seal-status. Produces: 200 application/json

        :return: The JSON response of the request.
        :rtype: dict
        """

    def read(self, path: str, wrap_ttl: int | str | None = None) -> dict[str, Any] | Response | None:
        """GET /<path>

        :param path:
        :type path:
        :param wrap_ttl:
        :type wrap_ttl:
        :return:
        :rtype:
        """

    def list(self, path: str) -> dict[str, Any] | Response | None:
        """GET /<path>?list=true

        :param path:
        :type path:
        :return:
        :rtype:
        """

    def write(self, path: str, wrap_ttl: int | str | None, **kwargs: Any) -> dict[str, Any] | Response:
        """POST /<path>

        Write data to a path. Because this method uses kwargs for the data to write, "path" and "wrap_ttl" data keys cannot be used.
        If these names are needed, or if the key names are not known at design time, consider using the write_data method.

        :param path:
        :type path: str
        :param wrap_ttl:
        :type wrap_ttl: str | None
        :param kwargs:
        :type kwargs: dict
        :return:
        :rtype:
        """

    def write_data(
        self, path: str, *, data: dict[str, Any] | None = None, wrap_ttl: int | str | None = None
    ) -> dict[str, Any] | Response:
        """Write data to a path. Similar to write() without restrictions on data keys.

        Supported methods:
            POST /<path>

        :param path:
        :type path: str
        :param data:
        :type data: dict | None
        :param wrap_ttl:
        :type wrap_ttl: str | None
        :return:
        :rtype:
        """

    def delete(self, path: str) -> None:
        """DELETE /<path>

        :param path:
        :type path:
        :return:
        :rtype:
        """

    @overload
    def get_policy(self, name: str, parse: Literal[False] = False) -> str | None:
        """Retrieve the policy body for the named policy.

        :param name: The name of the policy to retrieve.
        :type name: str | unicode
        :param parse: Specifies whether to parse the policy body using pyhcl or not.
        :type parse: bool
        :return: The (optionally parsed) policy body for the specified policy.
        :rtype: str | dict
        """

    @overload
    def get_policy(self, name: str, parse: Literal[True]) -> dict[str, Any] | None: ...
    def lookup_token(
        self, token: str | None = None, accessor: bool = False, wrap_ttl: int | str | None = None
    ) -> dict[str, Any] | Response:
        """GET /auth/token/lookup/<token>

        GET /auth/token/lookup-accessor/<token-accessor>

        GET /auth/token/lookup-self

        :param token:
        :type token: str.
        :param accessor:
        :type accessor: str.
        :param wrap_ttl:
        :type wrap_ttl: int.
        :return:
        :rtype:
        """

    def revoke_token(self, token: str, orphan: bool = False, accessor: bool = False) -> None:
        """POST /auth/token/revoke

        POST /auth/token/revoke-orphan

        POST /auth/token/revoke-accessor

        :param token:
        :type token:
        :param orphan:
        :type orphan:
        :param accessor:
        :type accessor:
        :return:
        :rtype:
        """

    def renew_token(
        self, token: str, increment: bool | None = None, wrap_ttl: int | str | None = None
    ) -> dict[str, Any] | Response:
        """POST /auth/token/renew

        POST /auth/token/renew-self

        :param token:
        :type token:
        :param increment:
        :type increment:
        :param wrap_ttl:
        :type wrap_ttl:
        :return:
        :rtype:

        For calls expecting to hit the renew-self endpoint please use the "renew_self" method on "hvac_client.auth.token" instead
        """

    def logout(self, revoke_token: bool = False) -> None:
        """Clears the token used for authentication, optionally revoking it before doing so.

        :param revoke_token:
        :type revoke_token:
        :return:
        :rtype:
        """

    def is_authenticated(self) -> bool:
        """Helper method which returns the authentication status of the client

        :return:
        :rtype:
        """

    def auth_cubbyhole(self, token: str) -> Response:
        """Perform a login request with a wrapped token.

        Stores the unwrapped token in the resulting Vault response for use by the :py:meth:`hvac.adapters.Adapter`
            instance under the _adapter Client attribute.

        :param token: Wrapped token
        :type token: str | unicode
        :return: The (JSON decoded) response of the auth request
        :rtype: dict
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
