"""
SSH Agent interface
"""

import sys
from _typeshed import ReadableBuffer
from collections.abc import Mapping
from logging import _ExcInfoType
from socket import _RetAddress, socket
from threading import Thread
from typing import Final, Protocol

from paramiko.channel import Channel
from paramiko.message import Message, _LikeBytes
from paramiko.pkey import PKey
from paramiko.transport import Transport

class _AgentProxy(Protocol):
    def connect(self) -> None: ...
    def close(self) -> None: ...

cSSH2_AGENTC_REQUEST_IDENTITIES: Final[bytes]
SSH2_AGENT_IDENTITIES_ANSWER: Final = 12
cSSH2_AGENTC_SIGN_REQUEST: Final[bytes]
SSH2_AGENT_SIGN_RESPONSE: Final = 14

SSH_AGENT_RSA_SHA2_256: Final = 2
SSH_AGENT_RSA_SHA2_512: Final = 4
ALGORITHM_FLAG_MAP: Final[dict[str, int]]
key: str
value: int

class AgentSSH:
    def __init__(self) -> None: ...
    def get_keys(self) -> tuple[AgentKey, ...]:
        """
        Return the list of keys available through the SSH agent, if any.  If
        no SSH agent was running (or it couldn't be contacted), an empty list
        will be returned.

        This method performs no IO, just returns the list of keys retrieved
        when the connection was made.

        :return:
            a tuple of `.AgentKey` objects representing keys available on the
            SSH agent
        """

class AgentProxyThread(Thread):
    """
    Class in charge of communication between two channels.
    """

    def __init__(self, agent: _AgentProxy) -> None: ...
    def run(self) -> None: ...

class AgentLocalProxy(AgentProxyThread):
    """
    Class to be used when wanting to ask a local SSH Agent being
    asked from a remote fake agent (so use a unix socket for ex.)
    """

    def __init__(self, agent: AgentServerProxy) -> None: ...
    def get_connection(self) -> tuple[socket, _RetAddress]:
        """
        Return a pair of socket object and string address.

        May block!
        """

class AgentRemoteProxy(AgentProxyThread):
    """
    Class to be used when wanting to ask a remote SSH Agent
    """

    def __init__(self, agent: AgentClientProxy, chan: Channel) -> None: ...
    def get_connection(self) -> tuple[socket, _RetAddress]: ...

if sys.platform == "win32":
    from .win_openssh import OpenSSHAgentConnection
    from .win_pageant import PageantConnection

    def get_agent_connection() -> PageantConnection | OpenSSHAgentConnection | None: ...

else:
    def get_agent_connection() -> socket | None:
        """
        Returns some SSH agent object, or None if none were found/supported.

        .. versionadded:: 2.10
        """

class AgentClientProxy:
    """
    Class proxying request as a client:

    #. client ask for a request_forward_agent()
    #. server creates a proxy and a fake SSH Agent
    #. server ask for establishing a connection when needed,
       calling the forward_agent_handler at client side.
    #. the forward_agent_handler launch a thread for connecting
       the remote fake agent and the local agent
    #. Communication occurs ...
    """

    thread: Thread
    def __init__(self, chanRemote: Channel) -> None: ...
    def __del__(self) -> None: ...
    def connect(self) -> None:
        """
        Method automatically called by ``AgentProxyThread.run``.
        """

    def close(self) -> None:
        """
        Close the current connection and terminate the agent
        Should be called manually
        """

class AgentServerProxy(AgentSSH):
    """
    Allows an SSH server to access a forwarded agent.

    This also creates a unix domain socket on the system to allow external
    programs to also access the agent. For this reason, you probably only want
    to create one of these.

    :meth:`connect` must be called before it is usable. This will also load the
    list of keys the agent contains. You must also call :meth:`close` in
    order to clean up the unix socket and the thread that maintains it.
    (:class:`contextlib.closing` might be helpful to you.)

    :param .Transport t: Transport used for SSH Agent communication forwarding

    :raises: `.SSHException` -- mostly if we lost the agent
    """

    thread: Thread
    def __init__(self, t: Transport) -> None: ...
    def __del__(self) -> None: ...
    def connect(self) -> None: ...
    def close(self) -> None:
        """
        Terminate the agent, clean the files, close connections
        Should be called manually
        """

    def get_env(self) -> dict[str, str]:
        """
        Helper for the environment under unix

        :return:
            a dict containing the ``SSH_AUTH_SOCK`` environment variables
        """

class AgentRequestHandler:
    """
    Primary/default implementation of SSH agent forwarding functionality.

    Simply instantiate this class, handing it a live command-executing session
    object, and it will handle forwarding any local SSH agent processes it
    finds.

    For example::

        # Connect
        client = SSHClient()
        client.connect(host, port, username)
        # Obtain session
        session = client.get_transport().open_session()
        # Forward local agent
        AgentRequestHandler(session)
        # Commands executed after this point will see the forwarded agent on
        # the remote end.
        session.exec_command("git clone https://my.git.repository/")
    """

    def __init__(self, chanClient: Channel) -> None: ...
    def __del__(self) -> None: ...
    def close(self) -> None: ...

class Agent(AgentSSH):
    """
    Client interface for using private keys from an SSH agent running on the
    local machine.  If an SSH agent is running, this class can be used to
    connect to it and retrieve `.PKey` objects which can be used when
    attempting to authenticate to remote SSH servers.

    Upon initialization, a session with the local machine's SSH agent is
    opened, if one is running. If no agent is running, initialization will
    succeed, but `get_keys` will return an empty tuple.

    :raises: `.SSHException` --
        if an SSH agent is found, but speaks an incompatible protocol

    .. versionchanged:: 2.10
        Added support for native openssh agent on windows (extending previous
        putty pageant support)
    """

    def __init__(self) -> None: ...
    def close(self) -> None:
        """
        Close the SSH agent connection.
        """

class AgentKey(PKey):
    """
    Private key held in a local SSH agent.  This type of key can be used for
    authenticating to a remote server (signing).  Most other key operations
    work as expected.

    .. versionchanged:: 3.2
        Added the ``comment`` kwarg and attribute.

    .. versionchanged:: 3.2
        Added the ``.inner_key`` attribute holding a reference to the 'real'
        key instance this key is a proxy for, if one was obtainable, else None.
    """

    agent: AgentSSH
    blob: bytes
    public_blob: None
    name: str
    comment: str
    def __init__(self, agent: AgentSSH, blob: ReadableBuffer, comment: str = "") -> None: ...
    def log(
        self,
        level: int,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None: ...
    def asbytes(self) -> bytes: ...
    def get_name(self) -> str: ...
    def sign_ssh_data(self, data: _LikeBytes, algorithm: str | None = None) -> Message: ...
