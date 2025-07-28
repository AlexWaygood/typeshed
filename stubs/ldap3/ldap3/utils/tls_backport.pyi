""" """

class CertificateError(ValueError): ...

def match_hostname(cert, hostname):
    """Backported from Python 3.4.3 standard library.

    Verify that *cert* (in decoded format as returned by
    SSLSocket.getpeercert()) matches the *hostname*.  RFC 2818 and RFC 6125
    rules are followed, but IP addresses are not accepted for *hostname*.

    CertificateError is raised on failure. On success, the function
    returns nothing.
    """
