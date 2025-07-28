"""
This module provides GSS-API / SSPI Key Exchange as defined in :rfc:`4462`.

.. note:: Credential delegation is not supported in server mode.

.. note::
    `RFC 4462 Section 2.2
    <https://tools.ietf.org/html/rfc4462.html#section-2.2>`_ says we are not
    required to implement GSS-API error messages. Thus, in many methods within
    this module, if an error occurs an exception will be thrown and the
    connection will be terminated.

.. seealso:: :doc:`/api/ssh_gss`

.. versionadded:: 1.15
"""

from paramiko.message import Message
from paramiko.ssh_gss import _SSH_GSSAuth
from paramiko.transport import Transport

MSG_KEXGSS_INIT: int
MSG_KEXGSS_CONTINUE: int
MSG_KEXGSS_COMPLETE: int
MSG_KEXGSS_HOSTKEY: int
MSG_KEXGSS_ERROR: int
MSG_KEXGSS_GROUPREQ: int
MSG_KEXGSS_GROUP: int

c_MSG_KEXGSS_INIT: bytes
c_MSG_KEXGSS_CONTINUE: bytes
c_MSG_KEXGSS_COMPLETE: bytes
c_MSG_KEXGSS_HOSTKEY: bytes
c_MSG_KEXGSS_ERROR: bytes
c_MSG_KEXGSS_GROUPREQ: bytes
c_MSG_KEXGSS_GROUP: bytes

class KexGSSGroup1:
    """
    GSS-API / SSPI Authenticated Diffie-Hellman Key Exchange as defined in `RFC
    4462 Section 2 <https://tools.ietf.org/html/rfc4462.html#section-2>`_
    """

    P: int
    G: int
    b7fffffffffffffff: bytes
    b0000000000000000: bytes
    NAME: str
    transport: Transport
    kexgss: _SSH_GSSAuth
    gss_host: str | None
    x: int
    e: int
    f: int
    def __init__(self, transport: Transport) -> None: ...
    def start_kex(self) -> None:
        """
        Start the GSS-API / SSPI Authenticated Diffie-Hellman Key Exchange.
        """

    def parse_next(self, ptype: int, m: Message) -> None:
        """
        Parse the next packet.

        :param ptype: The (string) type of the incoming packet
        :param `.Message` m: The packet content
        """

class KexGSSGroup14(KexGSSGroup1):
    """
    GSS-API / SSPI Authenticated Diffie-Hellman Group14 Key Exchange as defined
    in `RFC 4462 Section 2
    <https://tools.ietf.org/html/rfc4462.html#section-2>`_
    """

    P: int
    G: int
    NAME: str

class KexGSSGex:
    """
    GSS-API / SSPI Authenticated Diffie-Hellman Group Exchange as defined in
    `RFC 4462 Section 2 <https://tools.ietf.org/html/rfc4462.html#section-2>`_
    """

    NAME: str
    min_bits: int
    max_bits: int
    preferred_bits: int
    transport: Transport
    kexgss: _SSH_GSSAuth
    gss_host: str | None
    p: int | None
    q: int | None
    g: int | None
    x: int | None
    e: int | None
    f: int | None
    old_style: bool
    def __init__(self, transport: Transport) -> None: ...
    def start_kex(self) -> None:
        """
        Start the GSS-API / SSPI Authenticated Diffie-Hellman Group Exchange
        """

    def parse_next(self, ptype: int, m: Message) -> None:
        """
        Parse the next packet.

        :param ptype: The (string) type of the incoming packet
        :param `.Message` m: The packet content
        """

class NullHostKey:
    """
    This class represents the Null Host Key for GSS-API Key Exchange as defined
    in `RFC 4462 Section 5
    <https://tools.ietf.org/html/rfc4462.html#section-5>`_
    """

    key: str
    def __init__(self) -> None: ...
    def get_name(self) -> str: ...
