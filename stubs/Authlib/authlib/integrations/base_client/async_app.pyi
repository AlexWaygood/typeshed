from logging import Logger

from authlib.integrations.base_client.sync_app import OAuth1Base, OAuth2Base

log: Logger

__all__ = ["AsyncOAuth1Mixin", "AsyncOAuth2Mixin"]

class AsyncOAuth1Mixin(OAuth1Base):
    async def request(self, method, url, token=None, **kwargs): ...
    async def create_authorization_url(self, redirect_uri=None, **kwargs):
        """Generate the authorization url and state for HTTP redirect.

        :param redirect_uri: Callback or redirect URI for authorization.
        :param kwargs: Extra parameters to include.
        :return: dict
        """

    async def fetch_access_token(self, request_token=None, **kwargs):
        """Fetch access token in one step.

        :param request_token: A previous request token for OAuth 1.
        :param kwargs: Extra parameters to fetch access token.
        :return: A token dict.
        """

class AsyncOAuth2Mixin(OAuth2Base):
    async def load_server_metadata(self): ...
    async def request(self, method, url, token=None, **kwargs): ...
    async def create_authorization_url(self, redirect_uri=None, **kwargs):
        """Generate the authorization url and state for HTTP redirect.

        :param redirect_uri: Callback or redirect URI for authorization.
        :param kwargs: Extra parameters to include.
        :return: dict
        """

    async def fetch_access_token(self, redirect_uri=None, **kwargs):
        """Fetch access token in the final step.

        :param redirect_uri: Callback or Redirect URI that is used in
                             previous :meth:`authorize_redirect`.
        :param kwargs: Extra parameters to fetch access token.
        :return: A token dict.
        """
