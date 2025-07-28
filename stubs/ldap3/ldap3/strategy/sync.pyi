""" """

from typing import Any

from ..strategy.base import BaseStrategy

LDAP_MESSAGE_TEMPLATE: Any

class SyncStrategy(BaseStrategy):
    """
    This strategy is synchronous. You send the request and get the response
    Requests return a boolean value to indicate the result of the requested Operation
    Connection.response will contain the whole LDAP response for the messageId requested in a dict form
    Connection.request will contain the result LDAP message in a dict form
    """

    sync: bool
    no_real_dsa: bool
    pooled: bool
    can_stream: bool
    socket_size: Any
    def __init__(self, ldap_connection) -> None: ...
    def open(self, reset_usage: bool = True, read_server_info: bool = True) -> None: ...
    def receiving(self):
        """
        Receives data over the socket
        Checks if the socket is closed
        """

    def post_send_single_response(self, message_id):
        """
        Executed after an Operation Request (except Search)
        Returns the result message or None
        """

    def post_send_search(self, message_id):
        """
        Executed after a search request
        Returns the result message and store in connection.response the objects found
        """

    def set_stream(self, value) -> None: ...
    def get_stream(self) -> None: ...
