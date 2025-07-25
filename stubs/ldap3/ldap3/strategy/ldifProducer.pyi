""" """

from typing import Any

from .base import BaseStrategy

class LdifProducerStrategy(BaseStrategy):
    """
    This strategy is used to create the LDIF stream for the Add, Delete, Modify, ModifyDn operations.
    You send the request and get the request in the ldif-change representation of the operation.
    NO OPERATION IS SENT TO THE LDAP SERVER!
    Connection.request will contain the result LDAP message in a dict form
    Connection.response will contain the ldif-change format of the requested operation if available
    You don't need a real server to connect to for this strategy
    """

    sync: bool
    no_real_dsa: bool
    pooled: bool
    can_stream: bool
    line_separator: Any
    all_base64: bool
    stream: Any
    order: Any
    def __init__(self, ldap_connection) -> None: ...
    def receiving(self) -> None: ...
    def send(self, message_type, request, controls=None):
        """
        Build the LDAPMessage without sending to server
        """

    def post_send_single_response(self, message_id): ...
    def post_send_search(self, message_id) -> None: ...
    def accumulate_stream(self, fragment) -> None: ...
    def get_stream(self): ...
    def set_stream(self, value) -> None: ...
