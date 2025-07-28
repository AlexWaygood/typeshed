""" """

from threading import Thread
from typing import Any

from ..strategy.base import BaseStrategy

class AsyncStrategy(BaseStrategy):
    """
    This strategy is asynchronous. You send the request and get the messageId of the request sent
    Receiving data from socket is managed in a separated thread in a blocking mode
    Requests return an int value to indicate the messageId of the requested Operation
    You get the response with get_response, it has a timeout to wait for response to appear
    Connection.response will contain the whole LDAP response for the messageId requested in a dict form
    Connection.request will contain the result LDAP message in a dict form
    Response appear in strategy._responses dictionary
    """

    class ReceiverSocketThread(Thread):
        """
        The thread that actually manage the receiver socket
        """

        connection: Any
        socket_size: Any
        def __init__(self, ldap_connection) -> None: ...
        def run(self) -> None:
            """
            Waits for data on socket, computes the length of the message and waits for enough bytes to decode the message
            Message are appended to strategy._responses
            """

    sync: bool
    no_real_dsa: bool
    pooled: bool
    can_stream: bool
    receiver: Any
    async_lock: Any
    event_lock: Any
    def __init__(self, ldap_connection) -> None: ...
    def open(self, reset_usage: bool = True, read_server_info: bool = True) -> None:
        """
        Open connection and start listen on the socket in a different thread
        """

    def close(self) -> None:
        """
        Close connection and stop socket thread
        """

    def set_event_for_message(self, message_id) -> None: ...
    def post_send_search(self, message_id):
        """
        Clears connection.response and returns messageId
        """

    def post_send_single_response(self, message_id):
        """
        Clears connection.response and returns messageId.
        """

    def receiving(self) -> None: ...
    def get_stream(self) -> None: ...
    def set_stream(self, value) -> None: ...
