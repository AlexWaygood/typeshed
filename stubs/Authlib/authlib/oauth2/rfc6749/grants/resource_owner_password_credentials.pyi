from logging import Logger

from authlib.oauth2.rfc6749 import BaseGrant, TokenEndpointMixin

log: Logger

class ResourceOwnerPasswordCredentialsGrant(BaseGrant, TokenEndpointMixin):
    """The resource owner password credentials grant type is suitable in
    cases where the resource owner has a trust relationship with the
    client, such as the device operating system or a highly privileged.

    application.  The authorization server should take special care when
    enabling this grant type and only allow it when other flows are not
    viable.

    This grant type is suitable for clients capable of obtaining the
    resource owner's credentials (username and password, typically using
    an interactive form).  It is also used to migrate existing clients
    using direct authentication schemes such as HTTP Basic or Digest
    authentication to OAuth by converting the stored credentials to an
    access token::

        +----------+
        | Resource |
        |  Owner   |
        |          |
        +----------+
            v
            |    Resource Owner
           (A) Password Credentials
            |
            v
        +---------+                                  +---------------+
        |         |>--(B)---- Resource Owner ------->|               |
        |         |         Password Credentials     | Authorization |
        | Client  |                                  |     Server    |
        |         |<--(C)---- Access Token ---------<|               |
        |         |    (w/ Optional Refresh Token)   |               |
        +---------+                                  +---------------+
    """

    GRANT_TYPE: str
    def validate_token_request(self) -> None:
        """The client makes a request to the token endpoint by adding the
        following parameters using the "application/x-www-form-urlencoded"
        format per Appendix B with a character encoding of UTF-8 in the HTTP
        request entity-body:

        grant_type
             REQUIRED.  Value MUST be set to "password".

        username
             REQUIRED.  The resource owner username.

        password
             REQUIRED.  The resource owner password.

        scope
             OPTIONAL.  The scope of the access request as described by
             Section 3.3.

        If the client type is confidential or the client was issued client
        credentials (or assigned other authentication requirements), the
        client MUST authenticate with the authorization server as described
        in Section 3.2.1.

        For example, the client makes the following HTTP request using
        transport-layer security (with extra line breaks for display purposes
        only):

        .. code-block:: http

            POST /token HTTP/1.1
            Host: server.example.com
            Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
            Content-Type: application/x-www-form-urlencoded

            grant_type=password&username=johndoe&password=A3ddj3w
        """

    def create_token_response(self): ...
    def authenticate_user(self, username, password) -> None:
        """Validate the resource owner password credentials using its
        existing password validation algorithm::

            def authenticate_user(self, username, password):
                user = get_user_by_username(username)
                if user.check_password(password):
                    return user
        """
