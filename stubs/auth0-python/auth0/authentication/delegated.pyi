from .base import AuthenticationBase

class Delegated(AuthenticationBase):
    """Delegated authentication endpoints.

    Args:
        domain (str): Your auth0 domain (e.g: username.auth0.com)
    """

    def get_token(
        self,
        target: str,
        api_type: str,
        grant_type: str,
        id_token: str | None = None,
        refresh_token: str | None = None,
        scope: str = "openid",
    ):
        """Obtain a delegation token."""
