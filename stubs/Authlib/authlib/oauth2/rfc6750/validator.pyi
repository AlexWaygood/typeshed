"""authlib.oauth2.rfc6750.validator.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Validate Bearer Token for in request, scope and token.
"""

from authlib.oauth2.rfc6749 import TokenValidator

class BearerTokenValidator(TokenValidator):
    TOKEN_TYPE: str
    def authenticate_token(self, token_string) -> None:
        """A method to query token from database with the given token string.
        Developers MUST re-implement this method. For instance::

            def authenticate_token(self, token_string):
                return get_token_from_database(token_string)

        :param token_string: A string to represent the access_token.
        :return: token
        """

    def validate_token(self, token, scopes, request) -> None:
        """Check if token is active and matches the requested scopes."""
