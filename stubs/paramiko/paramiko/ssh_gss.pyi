"""
This module provides GSS-API / SSPI  authentication as defined in :rfc:`4462`.

.. note:: Credential delegation is not supported in server mode.

.. seealso:: :doc:`/api/kex_gss`

.. versionadded:: 1.15
"""

from typing import Any

GSS_AUTH_AVAILABLE: bool
GSS_EXCEPTIONS: tuple[type[Exception], ...]

def GSSAuth(auth_method: str, gss_deleg_creds: bool = True) -> _SSH_GSSAuth:
    """
    Provide SSH2 GSS-API / SSPI authentication.

    :param str auth_method: The name of the SSH authentication mechanism
                            (gssapi-with-mic or gss-keyex)
    :param bool gss_deleg_creds: Delegate client credentials or not.
                                 We delegate credentials by default.
    :return: Either an `._SSH_GSSAPI_OLD` or `._SSH_GSSAPI_NEW` (Unix)
             object or an `_SSH_SSPI` (Windows) object
    :rtype: object

    :raises: ``ImportError`` -- If no GSS-API / SSPI module could be imported.

    :see: `RFC 4462 <http://www.ietf.org/rfc/rfc4462.txt>`_
    :note: Check for the available API and return either an `._SSH_GSSAPI_OLD`
           (MIT GSSAPI using python-gssapi package) object, an
           `._SSH_GSSAPI_NEW` (MIT GSSAPI using gssapi package) object
           or an `._SSH_SSPI` (MS SSPI) object.
           If there is no supported API available,
           ``None`` will be returned.
    """

class _SSH_GSSAuth:
    """
    Contains the shared variables and methods of `._SSH_GSSAPI_OLD`,
    `._SSH_GSSAPI_NEW` and `._SSH_SSPI`.
    """

    cc_file: None
    def __init__(self, auth_method: str, gss_deleg_creds: bool) -> None:
        """
        :param str auth_method: The name of the SSH authentication mechanism
                                (gssapi-with-mic or gss-keyex)
        :param bool gss_deleg_creds: Delegate client credentials or not
        """

    def set_service(self, service: str) -> None:
        """
        This is just a setter to use a non default service.
        I added this method, because RFC 4462 doesn't specify "ssh-connection"
        as the only service value.

        :param str service: The desired SSH service
        """

    def set_username(self, username: str) -> None:
        """
        Setter for C{username}. If GSS-API Key Exchange is performed, the
        username is not set by C{ssh_init_sec_context}.

        :param str username: The name of the user who attempts to login
        """

    def ssh_gss_oids(self, mode: str = "client") -> bytes:
        """
        This method returns a single OID, because we only support the
        Kerberos V5 mechanism.

        :param str mode: Client for client mode and server for server mode
        :return: A byte sequence containing the number of supported
                 OIDs, the length of the OID and the actual OID encoded with
                 DER
        :note: In server mode we just return the OID length and the DER encoded
               OID.
        """

    def ssh_check_mech(self, desired_mech: str) -> bool:
        """
        Check if the given OID is the Kerberos V5 OID (server mode).

        :param str desired_mech: The desired GSS-API mechanism of the client
        :return: ``True`` if the given OID is supported, otherwise C{False}
        """

class _SSH_GSSAPI_OLD(_SSH_GSSAuth):
    """
    Implementation of the GSS-API MIT Kerberos Authentication for SSH2,
    using the older (unmaintained) python-gssapi package.

    :see: `.GSSAuth`
    """

    def __init__(self, auth_method: str, gss_deleg_creds: bool) -> None:
        """
        :param str auth_method: The name of the SSH authentication mechanism
                                (gssapi-with-mic or gss-keyex)
        :param bool gss_deleg_creds: Delegate client credentials or not
        """

    def ssh_init_sec_context(
        self, target: str, desired_mech: str | None = None, username: str | None = None, recv_token: str | None = None
    ) -> str | None:
        """
        Initialize a GSS-API context.

        :param str username: The name of the user who attempts to login
        :param str target: The hostname of the target to connect to
        :param str desired_mech: The negotiated GSS-API mechanism
                                 ("pseudo negotiated" mechanism, because we
                                 support just the krb5 mechanism :-))
        :param str recv_token: The GSS-API token received from the Server
        :raises:
            `.SSHException` -- Is raised if the desired mechanism of the client
            is not supported
        :return: A ``String`` if the GSS-API has returned a token or
            ``None`` if no token was returned
        """

    def ssh_get_mic(self, session_id: bytes, gss_kex: bool = False) -> Any:
        """
        Create the MIC token for a SSH2 message.

        :param str session_id: The SSH session ID
        :param bool gss_kex: Generate the MIC for GSS-API Key Exchange or not
        :return: gssapi-with-mic:
                 Returns the MIC token from GSS-API for the message we created
                 with ``_ssh_build_mic``.
                 gssapi-keyex:
                 Returns the MIC token from GSS-API with the SSH session ID as
                 message.
        """

    def ssh_accept_sec_context(self, hostname: str, recv_token: str, username: str | None = None) -> str | None:
        """
        Accept a GSS-API context (server mode).

        :param str hostname: The servers hostname
        :param str username: The name of the user who attempts to login
        :param str recv_token: The GSS-API Token received from the server,
                               if it's not the initial call.
        :return: A ``String`` if the GSS-API has returned a token or ``None``
                if no token was returned
        """

    def ssh_check_mic(self, mic_token: str, session_id: bytes, username: str | None = None) -> None:
        """
        Verify the MIC token for a SSH2 message.

        :param str mic_token: The MIC token received from the client
        :param str session_id: The SSH session ID
        :param str username: The name of the user who attempts to login
        :return: None if the MIC check was successful
        :raises: ``gssapi.GSSException`` -- if the MIC check failed
        """

    @property
    def credentials_delegated(self) -> bool:
        """
        Checks if credentials are delegated (server mode).

        :return: ``True`` if credentials are delegated, otherwise ``False``
        """

    def save_client_creds(self, client_token: str) -> None:
        """
        Save the Client token in a file. This is used by the SSH server
        to store the client credentials if credentials are delegated
        (server mode).

        :param str client_token: The GSS-API token received form the client
        :raises:
            ``NotImplementedError`` -- Credential delegation is currently not
            supported in server mode
        """

_SSH_GSSAPI = _SSH_GSSAPI_OLD

class _SSH_GSSAPI_NEW(_SSH_GSSAuth):
    """
    Implementation of the GSS-API MIT Kerberos Authentication for SSH2,
    using the newer, currently maintained gssapi package.

    :see: `.GSSAuth`
    """

    def __init__(self, auth_method: str, gss_deleg_creds: bool) -> None:
        """
        :param str auth_method: The name of the SSH authentication mechanism
                                (gssapi-with-mic or gss-keyex)
        :param bool gss_deleg_creds: Delegate client credentials or not
        """

    def ssh_init_sec_context(
        self, target: str, desired_mech: str | None = None, username: str | None = None, recv_token: str | None = None
    ) -> str:
        """
        Initialize a GSS-API context.

        :param str username: The name of the user who attempts to login
        :param str target: The hostname of the target to connect to
        :param str desired_mech: The negotiated GSS-API mechanism
                                 ("pseudo negotiated" mechanism, because we
                                 support just the krb5 mechanism :-))
        :param str recv_token: The GSS-API token received from the Server
        :raises: `.SSHException` -- Is raised if the desired mechanism of the
                 client is not supported
        :raises: ``gssapi.exceptions.GSSError`` if there is an error signaled
                                                by the GSS-API implementation
        :return: A ``String`` if the GSS-API has returned a token or ``None``
                 if no token was returned
        """

    def ssh_get_mic(self, session_id: bytes, gss_kex: bool = False) -> Any:
        """
        Create the MIC token for a SSH2 message.

        :param str session_id: The SSH session ID
        :param bool gss_kex: Generate the MIC for GSS-API Key Exchange or not
        :return: gssapi-with-mic:
                 Returns the MIC token from GSS-API for the message we created
                 with ``_ssh_build_mic``.
                 gssapi-keyex:
                 Returns the MIC token from GSS-API with the SSH session ID as
                 message.
        :rtype: str
        """

    def ssh_accept_sec_context(self, hostname: str, recv_token: str, username: str | None = None) -> str | None:
        """
        Accept a GSS-API context (server mode).

        :param str hostname: The servers hostname
        :param str username: The name of the user who attempts to login
        :param str recv_token: The GSS-API Token received from the server,
                               if it's not the initial call.
        :return: A ``String`` if the GSS-API has returned a token or ``None``
                if no token was returned
        """

    def ssh_check_mic(self, mic_token: str, session_id: bytes, username: str | None = None) -> None:
        """
        Verify the MIC token for a SSH2 message.

        :param str mic_token: The MIC token received from the client
        :param str session_id: The SSH session ID
        :param str username: The name of the user who attempts to login
        :return: None if the MIC check was successful
        :raises: ``gssapi.exceptions.GSSError`` -- if the MIC check failed
        """

    @property
    def credentials_delegated(self) -> bool:
        """
        Checks if credentials are delegated (server mode).

        :return: ``True`` if credentials are delegated, otherwise ``False``
        :rtype: bool
        """

    def save_client_creds(self, client_token: str) -> None:
        """
        Save the Client token in a file. This is used by the SSH server
        to store the client credentials if credentials are delegated
        (server mode).

        :param str client_token: The GSS-API token received form the client
        :raises: ``NotImplementedError`` -- Credential delegation is currently
                 not supported in server mode
        """

class _SSH_SSPI(_SSH_GSSAuth):
    """
    Implementation of the Microsoft SSPI Kerberos Authentication for SSH2.

    :see: `.GSSAuth`
    """

    def __init__(self, auth_method: str, gss_deleg_creds: bool) -> None:
        """
        :param str auth_method: The name of the SSH authentication mechanism
                                (gssapi-with-mic or gss-keyex)
        :param bool gss_deleg_creds: Delegate client credentials or not
        """

    def ssh_init_sec_context(
        self, target: str, desired_mech: str | None = None, username: str | None = None, recv_token: str | None = None
    ) -> str:
        """
        Initialize a SSPI context.

        :param str username: The name of the user who attempts to login
        :param str target: The FQDN of the target to connect to
        :param str desired_mech: The negotiated SSPI mechanism
                                 ("pseudo negotiated" mechanism, because we
                                 support just the krb5 mechanism :-))
        :param recv_token: The SSPI token received from the Server
        :raises:
            `.SSHException` -- Is raised if the desired mechanism of the client
            is not supported
        :return: A ``String`` if the SSPI has returned a token or ``None`` if
                 no token was returned
        """

    def ssh_get_mic(self, session_id: bytes, gss_kex: bool = False) -> Any:
        """
        Create the MIC token for a SSH2 message.

        :param str session_id: The SSH session ID
        :param bool gss_kex: Generate the MIC for Key Exchange with SSPI or not
        :return: gssapi-with-mic:
                 Returns the MIC token from SSPI for the message we created
                 with ``_ssh_build_mic``.
                 gssapi-keyex:
                 Returns the MIC token from SSPI with the SSH session ID as
                 message.
        """

    def ssh_accept_sec_context(self, hostname: str, username: str, recv_token: str) -> str | None:
        """
        Accept a SSPI context (server mode).

        :param str hostname: The servers FQDN
        :param str username: The name of the user who attempts to login
        :param str recv_token: The SSPI Token received from the server,
                               if it's not the initial call.
        :return: A ``String`` if the SSPI has returned a token or ``None`` if
                 no token was returned
        """

    def ssh_check_mic(self, mic_token: str, session_id: bytes, username: str | None = None) -> None:
        """
        Verify the MIC token for a SSH2 message.

        :param str mic_token: The MIC token received from the client
        :param str session_id: The SSH session ID
        :param str username: The name of the user who attempts to login
        :return: None if the MIC check was successful
        :raises: ``sspi.error`` -- if the MIC check failed
        """

    @property
    def credentials_delegated(self) -> bool:
        """
        Checks if credentials are delegated (server mode).

        :return: ``True`` if credentials are delegated, otherwise ``False``
        """

    def save_client_creds(self, client_token: str) -> None:
        """
        Save the Client token in a file. This is used by the SSH server
        to store the client credentails if credentials are delegated
        (server mode).

        :param str client_token: The SSPI token received form the client
        :raises:
            ``NotImplementedError`` -- Credential delegation is currently not
            supported in server mode
        """
