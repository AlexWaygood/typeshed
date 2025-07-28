"""authlib.oauth2.rfc6749.grants.refresh_token.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A special grant endpoint for refresh_token grant_type. Refreshing an
Access Token per `Section 6`_.

.. _`Section 6`: https://tools.ietf.org/html/rfc6749#section-6
"""

from logging import Logger
from typing_extensions import TypeAlias

from authlib.oauth2.rfc6749 import BaseGrant, TokenEndpointMixin, TokenMixin

_ServerResponse: TypeAlias = tuple[int, str, list[tuple[str, str]]]

log: Logger

class RefreshTokenGrant(BaseGrant, TokenEndpointMixin):
    """A special grant endpoint for refresh_token grant_type. Refreshing an
    Access Token per `Section 6`_.

    .. _`Section 6`: https://tools.ietf.org/html/rfc6749#section-6
    """

    GRANT_TYPE: str
    INCLUDE_NEW_REFRESH_TOKEN: bool
    def validate_token_request(self) -> None:
        """If the authorization server issued a refresh token to the client, the
        client makes a refresh request to the token endpoint by adding the
        following parameters using the "application/x-www-form-urlencoded"
        format per Appendix B with a character encoding of UTF-8 in the HTTP
        request entity-body, per Section 6:

        grant_type
             REQUIRED.  Value MUST be set to "refresh_token".

        refresh_token
             REQUIRED.  The refresh token issued to the client.

        scope
             OPTIONAL.  The scope of the access request as described by
             Section 3.3.  The requested scope MUST NOT include any scope
             not originally granted by the resource owner, and if omitted is
             treated as equal to the scope originally granted by the
             resource owner.


        For example, the client makes the following HTTP request using
        transport-layer security (with extra line breaks for display purposes
        only):

        .. code-block:: http

            POST /token HTTP/1.1
            Host: server.example.com
            Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
            Content-Type: application/x-www-form-urlencoded

            grant_type=refresh_token&refresh_token=tGzv3JOkF0XG5Qx2TlKWIA
        """

    def create_token_response(self) -> _ServerResponse: ...
    def issue_token(self, user, refresh_token: TokenMixin) -> dict[str, str | int]: ...
    def authenticate_refresh_token(self, refresh_token: str) -> TokenMixin:
        """Get token information with refresh_token string. Developers MUST
        implement this method in subclass::

            def authenticate_refresh_token(self, refresh_token):
                token = Token.get(refresh_token=refresh_token)
                if token and not token.refresh_token_revoked:
                    return token

        :param refresh_token: The refresh token issued to the client
        :return: token
        """

    def authenticate_user(self, refresh_token):
        """Authenticate the user related to this credential. Developers MUST
        implement this method in subclass::

            def authenticate_user(self, credential):
                return User.get(credential.user_id)

        :param refresh_token: Token object
        :return: user
        """

    def revoke_old_credential(self, refresh_token: TokenMixin) -> None:
        """The authorization server MAY revoke the old refresh token after
        issuing a new refresh token to the client. Developers MUST implement
        this method in subclass::

            def revoke_old_credential(self, refresh_token):
                credential.revoked = True
                credential.save()

        :param refresh_token: Token object
        """
