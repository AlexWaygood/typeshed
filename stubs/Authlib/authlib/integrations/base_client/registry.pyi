from _typeshed import Incomplete

from authlib.integrations.base_client import FrameworkIntegration

__all__ = ["BaseOAuth"]

class BaseOAuth:
    """Registry for oauth clients.

    Create an instance for registry::

        oauth = OAuth()
    """

    oauth1_client_cls: Incomplete
    oauth2_client_cls: Incomplete
    framework_integration_cls: type[FrameworkIntegration] = ...
    cache: Incomplete
    fetch_token: Incomplete
    update_token: Incomplete
    def __init__(self, cache=None, fetch_token=None, update_token=None) -> None: ...
    def create_client(self, name):
        """Create or get the given named OAuth client. For instance, the
        OAuth registry has ``.register`` a twitter client, developers may
        access the client with::

            client = oauth.create_client("twitter")

        :param: name: Name of the remote application
        :return: OAuth remote app
        """

    def register(self, name, overwrite: bool = False, **kwargs):
        """Registers a new remote application.

        :param name: Name of the remote application.
        :param overwrite: Overwrite existing config with framework settings.
        :param kwargs: Parameters for :class:`RemoteApp`.

        Find parameters for the given remote app class. When a remote app is
        registered, it can be accessed with *named* attribute::

            oauth.register('twitter', client_id='', ...)
            oauth.twitter.get('timeline')
        """

    def generate_client_kwargs(self, name, overwrite, **kwargs): ...
    def load_config(self, name, params): ...
    def __getattr__(self, key): ...
