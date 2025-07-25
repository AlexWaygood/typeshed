""" """

from threading import Thread
from typing import Any

from .base import BaseStrategy

TERMINATE_REUSABLE: str
BOGUS_BIND: int
BOGUS_UNBIND: int
BOGUS_EXTENDED: int
BOGUS_ABANDON: int

class ReusableStrategy(BaseStrategy):
    """
    A pool of reusable SyncWaitRestartable connections with lazy behaviour and limited lifetime.
    The connection using this strategy presents itself as a normal connection, but internally the strategy has a pool of
    connections that can be used as needed. Each connection lives in its own thread and has a busy/available status.
    The strategy performs the requested operation on the first available connection.
    The pool of connections is instantiated at strategy initialization.
    Strategy has two customizable properties, the total number of connections in the pool and the lifetime of each connection.
    When lifetime is expired the connection is closed and will be open again when needed.
    """

    pools: Any
    def receiving(self) -> None: ...
    def get_stream(self) -> None: ...
    def set_stream(self, value) -> None: ...

    class ConnectionPool:
        """
        Container for the Connection Threads
        """

        def __new__(cls, connection): ...
        name: Any
        master_connection: Any
        workers: Any
        pool_size: Any
        lifetime: Any
        keepalive: Any
        request_queue: Any
        open_pool: bool
        bind_pool: bool
        tls_pool: bool
        counter: int
        terminated_usage: Any
        terminated: bool
        pool_lock: Any
        started: bool
        def __init__(self, connection) -> None: ...
        def get_info_from_server(self) -> None: ...
        def rebind_pool(self) -> None: ...
        def start_pool(self): ...
        def create_pool(self) -> None: ...
        def terminate_pool(self) -> None: ...

    class PooledConnectionThread(Thread):
        """
        The thread that holds the Reusable connection and receive operation request via the queue
        Result are sent back in the pool._incoming list when ready
        """

        daemon: bool
        worker: Any
        master_connection: Any
        def __init__(self, worker, master_connection) -> None: ...
        def run(self) -> None: ...

    class PooledConnectionWorker:
        """
        Container for the restartable connection. it includes a thread and a lock to execute the connection in the pool
        """

        master_connection: Any
        request_queue: Any
        running: bool
        busy: bool
        get_info_from_server: bool
        connection: Any
        creation_time: Any
        task_counter: int
        thread: Any
        worker_lock: Any
        def __init__(self, connection, request_queue) -> None: ...
        def new_connection(self) -> None: ...

    sync: bool
    no_real_dsa: bool
    pooled: bool
    can_stream: bool
    pool: Any
    def __init__(self, ldap_connection) -> None: ...
    def open(self, reset_usage: bool = True, read_server_info: bool = True) -> None: ...
    def terminate(self) -> None: ...
    def send(self, message_type, request, controls=None): ...
    def validate_bind(self, controls): ...
    def get_response(self, counter, timeout=None, get_request: bool = False): ...
    def post_send_single_response(self, counter): ...
    def post_send_search(self, counter): ...
