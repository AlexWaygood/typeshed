from authlib.oauth2 import OAuth2Error

class InvalidRedirectURIError(OAuth2Error):
    """The value of one or more redirection URIs is invalid.
    https://tools.ietf.org/html/rfc7591#section-3.2.2.
    """

    error: str

class InvalidClientMetadataError(OAuth2Error):
    """The value of one of the client metadata fields is invalid and the
    server has rejected this request.  Note that an authorization
    server MAY choose to substitute a valid value for any requested
    parameter of a client's metadata.
    https://tools.ietf.org/html/rfc7591#section-3.2.2.
    """

    error: str

class InvalidSoftwareStatementError(OAuth2Error):
    """The software statement presented is invalid.
    https://tools.ietf.org/html/rfc7591#section-3.2.2.
    """

    error: str

class UnapprovedSoftwareStatementError(OAuth2Error):
    """The software statement presented is not approved for use by this
    authorization server.
    https://tools.ietf.org/html/rfc7591#section-3.2.2.
    """

    error: str
