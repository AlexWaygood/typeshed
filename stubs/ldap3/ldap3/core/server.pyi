""" """

from typing import Any, Literal

unix_socket_available: bool

class Server:
    """
    LDAP Server definition class

    Allowed_referral_hosts can be None (default), or a list of tuples of
    allowed servers ip address or names to contact while redirecting
    search to referrals.

    The second element of the tuple is a boolean to indicate if
    authentication to that server is allowed; if False only anonymous
    bind will be used.

    Per RFC 4516. Use [('*', False)] to allow any host with anonymous
    bind, use [('*', True)] to allow any host with same authentication of
    Server.
    """

    ipc: bool
    host: Any
    port: Any
    allowed_referral_hosts: Any
    ssl: Any
    tls: Any
    name: Any
    get_info: Any
    dit_lock: Any
    custom_formatter: Any
    custom_validator: Any
    current_address: Any
    connect_timeout: Any
    mode: Any
    def __init__(
        self,
        host: str,
        port: int | None = None,
        use_ssl: bool = False,
        allowed_referral_hosts=None,
        get_info: Literal["NO_INFO", "DSA", "SCHEMA", "ALL"] = "SCHEMA",
        tls=None,
        formatter=None,
        connect_timeout=None,
        mode: Literal["IP_SYSTEM_DEFAULT", "IP_V4_ONLY", "IP_V6_ONLY", "IP_V4_PREFERRED", "IP_V6_PREFERRED"] = "IP_V6_PREFERRED",
        validator=None,
    ) -> None: ...
    @property
    def address_info(self): ...
    def update_availability(self, address, available) -> None: ...
    def reset_availability(self) -> None: ...
    def check_availability(self, source_address=None, source_port=None, source_port_list=None):
        """
        Tries to open, connect and close a socket to specified address and port to check availability.
        Timeout in seconds is specified in CHECK_AVAILABITY_TIMEOUT if not specified in
        the Server object.
        If specified, use a specific address, port, or list of possible ports, when attempting to check availability.
        NOTE: This will only consider multiple ports from the source port list if the first ones we try to bind to are
              already in use. This will not attempt using different ports in the list if the server is unavailable,
              as that could result in the runtime of check_availability significantly exceeding the connection timeout.
        """

    @staticmethod
    def next_message_id():
        """
        LDAP messageId is unique for all connections to same server
        """

    def get_info_from_server(self, connection) -> None:
        """
        reads info from DSE and from subschema
        """

    def attach_dsa_info(self, dsa_info=None) -> None: ...
    def attach_schema_info(self, dsa_schema=None) -> None: ...
    @property
    def info(self): ...
    @property
    def schema(self): ...
    @staticmethod
    def from_definition(host, dsa_info, dsa_schema, port=None, use_ssl: bool = False, formatter=None, validator=None):
        """
        Define a dummy server with preloaded schema and info
        :param host: host name
        :param dsa_info: DsaInfo preloaded object or a json formatted string or a file name
        :param dsa_schema: SchemaInfo preloaded object or a json formatted string or a file name
        :param port: fake port
        :param use_ssl: use_ssl
        :param formatter: custom formatters
        :return: Server object
        """

    def candidate_addresses(self): ...
    def has_control(self, control): ...
    def has_extension(self, extension): ...
    def has_feature(self, feature): ...
