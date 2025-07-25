from authlib.oauth2.rfc6749 import TokenValidator

class IntrospectTokenValidator(TokenValidator):
    TOKEN_TYPE: str
    def introspect_token(self, token_string) -> None:
        """Request introspection token endpoint with the given token string,
        authorization server will return token information in JSON format.
        Developers MUST implement this method before using it::

            def introspect_token(self, token_string):
                # for example, introspection token endpoint has limited
                # internal IPs to access, so there is no need to add
                # authentication.
                url = "https://example.com/oauth/introspect"
                resp = requests.post(url, data={"token": token_string})
                resp.raise_for_status()
                return resp.json()
        """

    def authenticate_token(self, token_string): ...
    def validate_token(self, token, scopes, request) -> None: ...
