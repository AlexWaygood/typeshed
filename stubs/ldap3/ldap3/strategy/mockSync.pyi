""" """

from typing import Any

from .mockBase import MockBaseStrategy
from .sync import SyncStrategy

class MockSyncStrategy(MockBaseStrategy, SyncStrategy):
    """
    This strategy create a mock LDAP server, with synchronous access
    It can be useful to test LDAP without accessing a real Server
    """

    def __init__(self, ldap_connection) -> None: ...
    def post_send_search(self, payload): ...
    bound: Any
    def post_send_single_response(self, payload): ...
