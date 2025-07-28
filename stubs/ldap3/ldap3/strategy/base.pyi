""" """

from typing import Any

unix_socket_available: bool
SESSION_TERMINATED_BY_SERVER: str
TRANSACTION_ERROR: str
RESPONSE_COMPLETE: str

class BaseStrategy:
    """
    Base class for connection strategy
    """

    connection: Any
    sync: Any
    no_real_dsa: Any
    pooled: Any
    can_stream: Any
    referral_cache: Any
    thread_safe: bool
    def __init__(self, ldap_connection) -> None: ...
    def open(self, reset_usage: bool = True, read_server_info: bool = True) -> None:
        """
        Open a socket to a server. Choose a server from the server pool if available
        """

    def close(self) -> None:
        """
        Close connection
        """

    def send(self, message_type, request, controls=None):
        """
        Send an LDAP message
        Returns the message_id
        """

    def get_response(self, message_id, timeout=None, get_request: bool = False):
        """
        Get response LDAP messages
        Responses are returned by the underlying connection strategy
        Check if message_id LDAP message is still outstanding and wait for timeout to see if it appears in _get_response
        Result is stored in connection.result
        Responses without result is stored in connection.response
        A tuple (responses, result) is returned
        """

    @staticmethod
    def compute_ldap_message_size(data):
        """
        Compute LDAP Message size according to BER definite length rules
        Returns -1 if too few data to compute message length
        """

    def decode_response(self, ldap_message):
        """
        Convert received LDAPMessage to a dict
        """

    def decode_response_fast(self, ldap_message):
        """
        Convert received LDAPMessage from fast ber decoder to a dict
        """

    @staticmethod
    def decode_control(control):
        """
        decode control, return a 2-element tuple where the first element is the control oid
        and the second element is a dictionary with description (from Oids), criticality and decoded control value
        """

    @staticmethod
    def decode_control_fast(control, from_server: bool = True):
        """
        decode control, return a 2-element tuple where the first element is the control oid
        and the second element is a dictionary with description (from Oids), criticality and decoded control value
        """

    @staticmethod
    def decode_request(message_type, component, controls=None): ...
    def valid_referral_list(self, referrals): ...
    def do_next_range_search(self, request, response, attr_name): ...
    def do_search_on_auto_range(self, request, response): ...
    def create_referral_connection(self, referrals): ...
    def do_operation_on_referral(self, request, referrals): ...
    def sending(self, ldap_message) -> None: ...
    def receiving(self) -> None: ...
    def post_send_single_response(self, message_id) -> None: ...
    def post_send_search(self, message_id) -> None: ...
    def get_stream(self) -> None: ...
    def set_stream(self, value) -> None: ...
    def unbind_referral_cache(self) -> None: ...
