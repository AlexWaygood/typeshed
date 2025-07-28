DAEMON_ADDRESS_KEY: str
DEFAULT_ADDRESS: str

class DaemonConfig:
    """The class that stores X-Ray daemon configuration about
    the ip address and port for UDP and TCP port. It gets the address
    string from ``AWS_TRACING_DAEMON_ADDRESS`` and then from recorder's
    configuration for ``daemon_address``.
    A notation of '127.0.0.1:2000' or 'tcp:127.0.0.1:2000 udp:127.0.0.2:2001'
    are both acceptable. The former one means UDP and TCP are running at
    the same address.
    By default it assumes a X-Ray daemon running at 127.0.0.1:2000
    listening to both UDP and TCP traffic.
    """

    def __init__(self, daemon_address="127.0.0.1:2000") -> None: ...
    @property
    def udp_ip(self): ...
    @property
    def udp_port(self): ...
    @property
    def tcp_ip(self): ...
    @property
    def tcp_port(self): ...
