"""A client for NDB which manages credentials, project, namespace, and database."""

from _typeshed import Incomplete
from collections.abc import Callable, Generator
from contextlib import contextmanager
from typing import ClassVar

from google.cloud.ndb import context as context_module, key

DATASTORE_API_HOST: str

class Client:
    """An NDB client.

    The NDB client must be created in order to use NDB, and any use of NDB must
    be within the context of a call to :meth:`context`.

    The Datastore Emulator is used for the client if and only if the
    DATASTORE_EMULATOR_HOST environment variable is set.

    Arguments:
        project (Optional[str]): The project to pass to proxied API methods. If
            not passed, falls back to the default inferred from the
            environment.
        namespace (Optional[str]): Namespace to pass to proxied API methods.
        credentials (Optional[:class:`~google.auth.credentials.Credentials`]):
            The OAuth2 Credentials to use for this client. If not passed, falls
            back to the default inferred from the environment.
        client_options (Optional[:class:`~google.api_core.client_options.ClientOptions` or :class:`dict`])
            Client options used to set user options on the client.
            API Endpoint should be set through client_options.
        database (Optional[str]): Database to access. Defaults to the (default) database.
    """

    SCOPE: ClassVar[tuple[str, ...]]
    namespace: str | None
    host: str
    client_info: Incomplete
    secure: bool
    stub: Incomplete
    database: str | None
    def __init__(
        self,
        project: str | None = ...,
        namespace: str | None = ...,
        credentials: Incomplete | None = ...,
        client_options: Incomplete | None = ...,
        database: str | None = None,
    ) -> None: ...
    @contextmanager
    def context(
        self,
        namespace=...,
        cache_policy: Callable[[key.Key], bool] | None = ...,
        global_cache: Incomplete | None = ...,
        global_cache_policy: Callable[[key.Key], bool] | None = ...,
        global_cache_timeout_policy: Callable[[key.Key], int] | None = ...,
        legacy_data: bool = ...,
    ) -> Generator[context_module.Context]:
        """Establish a context for a set of NDB calls.

        This method provides a context manager which establishes the runtime
        state for using NDB.

        For example:

        .. code-block:: python

            from google.cloud import ndb

            client = ndb.Client()
            with client.context():
                # Use NDB for some stuff
                pass

        Use of a context is required--NDB can only be used inside a running
        context. The context is used to manage the connection to Google Cloud
        Datastore, an event loop for asynchronous API calls, runtime caching
        policy, and other essential runtime state.

        Code within an asynchronous context should be single threaded.
        Internally, a :class:`threading.local` instance is used to track the
        current event loop.

        In a web application, it is recommended that a single context be used
        per HTTP request. This can typically be accomplished in a middleware
        layer.

        Arguments:
            cache_policy (Optional[Callable[[key.Key], bool]]): The
                cache policy to use in this context. See:
                :meth:`~google.cloud.ndb.context.Context.set_cache_policy`.
            global_cache (Optional[global_cache.GlobalCache]):
                The global cache for this context. See:
                :class:`~google.cloud.ndb.global_cache.GlobalCache`.
            global_cache_policy (Optional[Callable[[key.Key], bool]]): The
                global cache policy to use in this context. See:
                :meth:`~google.cloud.ndb.context.Context.set_global_cache_policy`.
            global_cache_timeout_policy (Optional[Callable[[key.Key], int]]):
                The global cache timeout to use in this context. See:
                :meth:`~google.cloud.ndb.context.Context.set_global_cache_timeout_policy`.
            legacy_data (bool): Set to ``True`` (the default) to write data in
                a way that can be read by the legacy version of NDB.
        """
