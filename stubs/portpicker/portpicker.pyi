"""Pure python code for finding unused ports on a host.

This module provides a pick_unused_port() function.
It can also be called via the command line for use in shell scripts.
When called from the command line, it takes one optional argument, which,
if given, is sent to portserver instead of portpicker's PID.
To reserve a port for the lifetime of a bash script, use $BASHPID as this
argument.

There is a race condition between picking a port and your application code
binding to it.  The use of a port server to prevent that is recommended on
loaded test hosts running many tests at a time.

If your code can accept a bound socket as input rather than being handed a
port number consider using socket.bind(('localhost', 0)) to bind to an
available port without a race condition rather than using this library.

Typical usage:
  test_port = portpicker.pick_unused_port()
"""

import socket
from typing_extensions import TypeAlias

_Port: TypeAlias = int

__all__ = ("bind", "is_port_free", "pick_unused_port", "return_port", "add_reserved_port", "get_port_from_port_server")

class NoFreePortFoundError(Exception):
    """Exception indicating that no free port could be found."""

def add_reserved_port(port: _Port) -> None:
    """Add a port that was acquired by means other than the port server."""

def return_port(port: _Port) -> None:
    """Return a port that is no longer being used so it can be reused."""

def bind(port: _Port, socket_type: socket.SocketKind, socket_proto: int) -> _Port | None:
    """Try to bind to a socket of the specified type, protocol, and port.

    This is primarily a helper function for PickUnusedPort, used to see
    if a particular port number is available.

    For the port to be considered available, the kernel must support at least
    one of (IPv6, IPv4), and the port must be available on each supported
    family.

    Args:
      port: The port number to bind to, or 0 to have the OS pick a free port.
      socket_type: The type of the socket (ex: socket.SOCK_STREAM).
      socket_proto: The protocol of the socket (ex: socket.IPPROTO_TCP).

    Returns:
      The port number on success or None on failure.
    """

def is_port_free(port: _Port) -> bool:
    """Check if specified port is free.

    Args:
      port: integer, port to check

    Returns:
      bool, whether port is free to use for both TCP and UDP.
    """

def pick_unused_port(pid: int | None = None, portserver_address: str | None = None) -> _Port:
    """Picks an unused port and reserves it for use by a given process id.

    Args:
      pid: PID to tell the portserver to associate the reservation with. If
        None, the current process's PID is used.
      portserver_address: The address (path) of a unix domain socket
        with which to connect to a portserver, a leading '@'
        character indicates an address in the "abstract namespace".  OR
        On systems without socket.AF_UNIX, this is an AF_INET address.
        If None, or no port is returned by the portserver at the provided
        address, the environment will be checked for a PORTSERVER_ADDRESS
        variable.  If that is not set, no port server will be used.

    If no portserver is used, no pid based reservation is managed by any
    central authority. Race conditions and duplicate assignments may occur.

    Returns:
      A port number that is unused on both TCP and UDP.

    Raises:
      NoFreePortFoundError: No free port could be found.
    """

def get_port_from_port_server(portserver_address: str, pid: int | None = None) -> _Port | None:
    """Request a free a port from a system-wide portserver.

    This follows a very simple portserver protocol:
    The request consists of our pid (in ASCII) followed by a newline.
    The response is a port number and a newline, 0 on failure.

    This function is an implementation detail of pick_unused_port().
    It should not normally be called by code outside of this module.

    Args:
      portserver_address: The address (path) of a unix domain socket
        with which to connect to the portserver.  A leading '@'
        character indicates an address in the "abstract namespace."
        On systems without socket.AF_UNIX, this is an AF_INET address.
      pid: The PID to tell the portserver to associate the reservation with.
        If None, the current process's PID is used.

    Returns:
      The port number on success or None on failure.
    """

# legacy aliases
Bind = bind
GetPortFromPortServer = get_port_from_port_server
IsPortFree = is_port_free
PickUnusedPort = pick_unused_port
