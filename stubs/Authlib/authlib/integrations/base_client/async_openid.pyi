__all__ = ["AsyncOpenIDMixin"]

class AsyncOpenIDMixin:
    async def fetch_jwk_set(self, force: bool = False): ...
    async def userinfo(self, **kwargs):
        """Fetch user info from ``userinfo_endpoint``."""

    async def parse_id_token(self, token, nonce, claims_options=None, claims_cls=None, leeway: int = 120):
        """Return an instance of UserInfo from token's ``id_token``."""
