from logging import Logger

from authlib.oauth2.rfc6749 import BaseGrant, TokenEndpointMixin

log: Logger

class ClientCredentialsGrant(BaseGrant, TokenEndpointMixin):
    """The client can request an access token using only its client
    credentials (or other supported means of authentication) when the
    client is requesting access to the protected resources under its
    control, or those of another resource owner that have been previously
    arranged with the authorization server.

    The client credentials grant type MUST only be used by confidential
    clients::

        +---------+                                  +---------------+
        |         |                                  |               |
        |         |>--(A)- Client Authentication --->| Authorization |
        | Client  |                                  |     Server    |
        |         |<--(B)---- Access Token ---------<|               |
        |         |                                  |               |
        +---------+                                  +---------------+

    https://tools.ietf.org/html/rfc6749#section-4.4
    """

    GRANT_TYPE: str
    def validate_token_request(self) -> None:
        """The client makes a request to the token endpoint by adding the
        following parameters using the "application/x-www-form-urlencoded"
        format per Appendix B with a character encoding of UTF-8 in the HTTP
        request entity-body:

        grant_type
             REQUIRED.  Value MUST be set to "client_credentials".

        scope
             OPTIONAL.  The scope of the access request as described by
             Section 3.3.

        The client MUST authenticate with the authorization server as
        described in Section 3.2.1.

        For example, the client makes the following HTTP request using
        transport-layer security (with extra line breaks for display purposes
        only):

        .. code-block:: http

            POST /token HTTP/1.1
            Host: server.example.com
            Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
            Content-Type: application/x-www-form-urlencoded

            grant_type=client_credentials

        The authorization server MUST authenticate the client.
        """

    def create_token_response(self): ...
