""" """

from _collections_abc import Generator, dict_keys
from _typeshed import Incomplete, ReadableBuffer
from types import TracebackType
from typing import Literal
from typing_extensions import Self, TypeAlias

from pyasn1.type.base import Asn1Item

from .pooling import ServerPool
from .server import Server

SASL_AVAILABLE_MECHANISMS: Incomplete
CLIENT_STRATEGIES: Incomplete

_ServerSequence: TypeAlias = (
    set[Server] | list[Server] | tuple[Server, ...] | Generator[Server, None, None] | dict_keys[Server, Incomplete]
)

class Connection:
    """Main ldap connection class.

    Controls, if used, must be a list of tuples. Each tuple must have 3
    elements, the control OID, a boolean meaning if the control is
    critical, a value.

    If the boolean is set to True the server must honor the control or
    refuse the operation

    Mixing controls must be defined in controls specification (as per
    RFC 4511)

    :param server: the Server object to connect to
    :type server: Server, str
    :param user: the user name for simple authentication
    :type user: str
    :param password: the password for simple authentication
    :type password: str
    :param auto_bind: specify if the bind will be performed automatically when defining the Connection object
    :type auto_bind: int, can be one of AUTO_BIND_DEFAULT, AUTO_BIND_NONE, AUTO_BIND_NO_TLS, AUTO_BIND_TLS_BEFORE_BIND, AUTO_BIND_TLS_AFTER_BIND as specified in ldap3
    :param version: LDAP version, default to 3
    :type version: int
    :param authentication: type of authentication
    :type authentication: int, can be one of ANONYMOUS, SIMPLE or SASL, as specified in ldap3
    :param client_strategy: communication strategy used in the Connection
    :type client_strategy: can be one of SYNC, ASYNC, LDIF, RESTARTABLE, REUSABLE as specified in ldap3
    :param auto_referrals: specify if the connection object must automatically follow referrals
    :type auto_referrals: bool
    :param sasl_mechanism: mechanism for SASL authentication, can be one of 'EXTERNAL', 'DIGEST-MD5', 'GSSAPI', 'PLAIN'
    :type sasl_mechanism: str
    :param sasl_credentials: credentials for SASL mechanism
    :type sasl_credentials: tuple
    :param check_names: if True the library will check names of attributes and object classes against the schema. Also values found in entries will be formatted as indicated by the schema
    :type check_names: bool
    :param collect_usage: collect usage metrics in the usage attribute
    :type collect_usage: bool
    :param read_only: disable operations that modify data in the LDAP server
    :type read_only: bool
    :param lazy: open and bind the connection only when an actual operation is performed
    :type lazy: bool
    :param raise_exceptions: raise exceptions when operations are not successful, if False operations return False if not successful but not raise exceptions
    :type raise_exceptions: bool
    :param pool_name: pool name for pooled strategies
    :type pool_name: str
    :param pool_size: pool size for pooled strategies
    :type pool_size: int
    :param pool_lifetime: pool lifetime for pooled strategies
    :type pool_lifetime: int
    :param cred_store: credential store for gssapi
    :type cred_store: dict
    :param use_referral_cache: keep referral connections open and reuse them
    :type use_referral_cache: bool
    :param auto_escape: automatic escaping of filter values
    :type auto_escape: bool
    :param auto_encode: automatic encoding of attribute values
    :type auto_encode: bool
    :param source_address: the ip address or hostname to use as the source when opening the connection to the server
    :type source_address: str
    :param source_port: the source port to use when opening the connection to the server. Cannot be specified with source_port_list
    :type source_port: int
    :param source_port_list: a list of source ports to choose from when opening the connection to the server. Cannot be specified with source_port
    :type source_port_list: list
    """

    connection_lock: Incomplete
    last_error: str
    strategy_type: Incomplete
    user: Incomplete
    password: Incomplete
    authentication: Incomplete
    version: Incomplete
    auto_referrals: Incomplete
    request: Incomplete
    response: Incomplete | None
    result: Incomplete
    bound: bool
    listening: bool
    closed: bool
    auto_bind: Incomplete
    sasl_mechanism: Incomplete
    sasl_credentials: Incomplete
    socket: Incomplete
    tls_started: bool
    sasl_in_progress: bool
    read_only: Incomplete
    lazy: Incomplete
    pool_name: Incomplete
    pool_size: int | None
    cred_store: Incomplete
    pool_lifetime: Incomplete
    pool_keepalive: Incomplete
    starting_tls: bool
    check_names: Incomplete
    raise_exceptions: Incomplete
    auto_range: Incomplete
    extend: Incomplete
    fast_decoder: Incomplete
    receive_timeout: Incomplete
    empty_attributes: Incomplete
    use_referral_cache: Incomplete
    auto_escape: Incomplete
    auto_encode: Incomplete
    source_address: Incomplete
    source_port_list: Incomplete
    server_pool: Incomplete | None
    server: Incomplete
    strategy: Incomplete
    send: Incomplete
    open: Incomplete
    get_response: Incomplete
    post_send_single_response: Incomplete
    post_send_search: Incomplete
    def __init__(
        self,
        server: Server | str | _ServerSequence | ServerPool,
        user: str | None = None,
        password: str | None = None,
        auto_bind: Literal["DEFAULT", "NONE", "NO_TLS", "TLS_BEFORE_BIND", "TLS_AFTER_BIND"] | bool = "DEFAULT",
        version: int = 3,
        authentication: Literal["ANONYMOUS", "SIMPLE", "SASL", "NTLM"] | None = None,
        client_strategy: Literal[
            "SYNC",
            "SAFE_RESTARTABLE",
            "SAFE_SYNC",
            "ASYNC",
            "LDIF",
            "RESTARTABLE",
            "REUSABLE",
            "MOCK_SYNC",
            "MOCK_ASYNC",
            "ASYNC_STREAM",
        ] = "SYNC",
        auto_referrals: bool = True,
        auto_range: bool = True,
        sasl_mechanism: str | None = None,
        sasl_credentials=None,
        check_names: bool = True,
        collect_usage: bool = False,
        read_only: bool = False,
        lazy: bool = False,
        raise_exceptions: bool = False,
        pool_name: str | None = None,
        pool_size: int | None = None,
        pool_lifetime: int | None = None,
        cred_store=None,
        fast_decoder: bool = True,
        receive_timeout=None,
        return_empty_attributes: bool = True,
        use_referral_cache: bool = False,
        auto_escape: bool = True,
        auto_encode: bool = True,
        pool_keepalive=None,
        source_address: str | None = None,
        source_port: int | None = None,
        source_port_list=None,
    ) -> None: ...
    def repr_with_sensitive_data_stripped(self): ...
    @property
    def stream(self):
        """Used by the LDIFProducer strategy to accumulate the ldif-change operations with a single LDIF header
        :return: reference to the response stream if defined in the strategy.
        """

    @stream.setter
    def stream(self, value) -> None: ...
    @property
    def usage(self):
        """Usage statistics for the connection.
        :return: Usage object
        """

    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> Literal[False] | None: ...
    def bind(self, read_server_info: bool = True, controls=None):
        """Bind to ldap Server with the authentication method and the user defined in the connection

        :param read_server_info: reads info from server
        :param controls: LDAP controls to send along with the bind operation
        :type controls: list of tuple
        :return: bool

        """

    def rebind(
        self,
        user=None,
        password=None,
        authentication=None,
        sasl_mechanism=None,
        sasl_credentials=None,
        read_server_info: bool = True,
        controls=None,
    ): ...
    def unbind(self, controls=None):
        """Unbind the connected user. Unbind implies closing session as per RFC4511 (4.3)

        :param controls: LDAP controls to send along with the bind operation

        """

    def search(
        self,
        search_base: str,
        search_filter: str,
        search_scope: Literal["BASE", "LEVEL", "SUBTREE"] = "SUBTREE",
        dereference_aliases: Literal["NEVER", "SEARCH", "FINDING_BASE", "ALWAYS"] = "ALWAYS",
        attributes=None,
        size_limit: int = 0,
        time_limit: int = 0,
        types_only: bool = False,
        get_operational_attributes: bool = False,
        controls=None,
        paged_size: int | None = None,
        paged_criticality: bool = False,
        paged_cookie: str | bytes | None = None,
        auto_escape: bool | None = None,
    ):
        """
        Perform an ldap search:

        - If attributes is empty noRFC2696 with the specified size
        - If paged is 0 and cookie is present the search is abandoned on
          server attribute is returned
        - If attributes is ALL_ATTRIBUTES all attributes are returned
        - If paged_size is an int greater than 0 a simple paged search
          is tried as described in
        - Cookie is an opaque string received in the last paged search
          and must be used on the next paged search response
        - If lazy == True open and bind will be deferred until another
          LDAP operation is performed
        - If mssing_attributes == True then an attribute not returned by the server is set to None
        - If auto_escape is set it overrides the Connection auto_escape
        """

    def compare(self, dn, attribute, value, controls=None):
        """
        Perform a compare operation
        """

    def add(self, dn, object_class=None, attributes=None, controls=None):
        """
        Add dn to the DIT, object_class is None, a class name or a list
        of class names.

        Attributes is a dictionary in the form 'attr': 'val' or 'attr':
        ['val1', 'val2', ...] for multivalued attributes
        """

    def delete(self, dn, controls=None):
        """
        Delete the entry identified by the DN from the DIB.
        """

    def modify(self, dn, changes, controls=None):
        """
        Modify attributes of entry

        - changes is a dictionary in the form {'attribute1': change), 'attribute2': [change, change, ...], ...}
        - change is (operation, [value1, value2, ...])
        - operation is 0 (MODIFY_ADD), 1 (MODIFY_DELETE), 2 (MODIFY_REPLACE), 3 (MODIFY_INCREMENT)
        """

    def modify_dn(self, dn, relative_dn, delete_old_dn: bool = True, new_superior=None, controls=None):
        """
        Modify DN of the entry or performs a move of the entry in the
        DIT.
        """

    def abandon(self, message_id, controls=None):
        """
        Abandon the operation indicated by message_id
        """

    def extended(
        self, request_name, request_value: Asn1Item | ReadableBuffer | None = None, controls=None, no_encode: bool | None = None
    ):
        """
        Performs an extended operation
        """

    def start_tls(self, read_server_info: bool = True): ...
    def do_sasl_bind(self, controls): ...
    def do_ntlm_bind(self, controls): ...
    def refresh_server_info(self) -> None: ...
    def response_to_ldif(
        self, search_result=None, all_base64: bool = False, line_separator=None, sort_order=None, stream=None
    ): ...
    def response_to_json(
        self,
        raw: bool = False,
        search_result=None,
        indent: int = 4,
        sort: bool = True,
        stream=None,
        checked_attributes: bool = True,
        include_empty: bool = True,
    ): ...
    def response_to_file(self, target, raw: bool = False, indent: int = 4, sort: bool = True) -> None: ...
    @property
    def entries(self): ...
