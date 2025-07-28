from authlib.oauth2.rfc6749 import TokenEndpoint

class RevocationEndpoint(TokenEndpoint):
    """Implementation of revocation endpoint which is described in
    `RFC7009`_.

    .. _RFC7009: https://tools.ietf.org/html/rfc7009
    """

    ENDPOINT_NAME: str
    def authenticate_token(self, request, client):
        """The client constructs the request by including the following
        parameters using the "application/x-www-form-urlencoded" format in
        the HTTP request entity-body:

        token
            REQUIRED.  The token that the client wants to get revoked.

        token_type_hint
            OPTIONAL.  A hint about the type of the token submitted for
            revocation.
        """

    def check_params(self, request, client) -> None: ...
    def create_endpoint_response(self, request):
        """Validate revocation request and create the response for revocation.
        For example, a client may request the revocation of a refresh token
        with the following request::

            POST /revoke HTTP/1.1
            Host: server.example.com
            Content-Type: application/x-www-form-urlencoded
            Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW

            token=45ghiukldjahdnhzdauz&token_type_hint=refresh_token

        :returns: (status_code, body, headers)
        """

    def query_token(self, token_string, token_type_hint) -> None:
        """Get the token from database/storage by the given token string.
        Developers should implement this method::

            def query_token(self, token_string, token_type_hint):
                if token_type_hint == 'access_token':
                    return Token.query_by_access_token(token_string)
                if token_type_hint == 'refresh_token':
                    return Token.query_by_refresh_token(token_string)
                return Token.query_by_access_token(token_string) or                     Token.query_by_refresh_token(token_string)
        """

    def revoke_token(self, token, request) -> None:
        """Mark token as revoked. Since token MUST be unique, it would be
        dangerous to delete it. Consider this situation:

        1. Jane obtained a token XYZ
        2. Jane revoked (deleted) token XYZ
        3. Bob generated a new token XYZ
        4. Jane can use XYZ to access Bob's resource

        It would be secure to mark a token as revoked::

            def revoke_token(self, token, request):
                hint = request.form.get("token_type_hint")
                if hint == "access_token":
                    token.access_token_revoked = True
                else:
                    token.access_token_revoked = True
                    token.refresh_token_revoked = True
                token.save()
        """
