""" """

posix_gssapi_unavailable: bool
windows_gssapi_unavailable: bool
NO_SECURITY_LAYER: int
INTEGRITY_PROTECTION: int
CONFIDENTIALITY_PROTECTION: int

def get_channel_bindings(ssl_socket): ...
def sasl_gssapi(connection, controls):
    """
    Performs a bind using the Kerberos v5 ("GSSAPI") SASL mechanism
    from RFC 4752. Does not support any security layers, only authentication!

    sasl_credentials can be empty or a tuple with one or two elements.
    The first element determines which service principal to request a ticket for and can be one of the following:

    - None or False, to use the hostname from the Server object
    - True to perform a reverse DNS lookup to retrieve the canonical hostname for the hosts IP address
    - A string containing the hostname

    The optional second element is what authorization ID to request.

    - If omitted or None, the authentication ID is used as the authorization ID
    - If a string, the authorization ID to use. Should start with "dn:" or "user:".

    The optional third element is a raw gssapi credentials structure which can be used over
    the implicit use of a krb ccache.
    """
