from collections.abc import Sequence

from docker.context.context import Context
from docker.tls import TLSConfig

class ContextAPI:
    """Context API.
    Contains methods for context management:
    create, list, remove, get, inspect.
    """

    DEFAULT_CONTEXT: Context
    @classmethod
    def create_context(
        cls,
        name: str,
        orchestrator: str | None = None,
        host: str | None = None,
        tls_cfg: TLSConfig | None = None,
        default_namespace: str | None = None,
        skip_tls_verify: bool = False,
    ) -> Context:
        """Creates a new context.
        Returns:
            (Context): a Context object.
        Raises:
            :py:class:`docker.errors.MissingContextParameter`
                If a context name is not provided.
            :py:class:`docker.errors.ContextAlreadyExists`
                If a context with the name already exists.
            :py:class:`docker.errors.ContextException`
                If name is default.

        Example:

        >>> from docker.context import ContextAPI
        >>> ctx = ContextAPI.create_context(name='test')
        >>> print(ctx.Metadata)
        {
            "Name": "test",
            "Metadata": {},
            "Endpoints": {
                "docker": {
                    "Host": "unix:///var/run/docker.sock",
                    "SkipTLSVerify": false
                }
            }
        }
        """

    @classmethod
    def get_context(cls, name: str | None = None) -> Context:
        """Retrieves a context object.
        Args:
            name (str): The name of the context

        Example:

        >>> from docker.context import ContextAPI
        >>> ctx = ContextAPI.get_context(name='test')
        >>> print(ctx.Metadata)
        {
            "Name": "test",
            "Metadata": {},
            "Endpoints": {
                "docker": {
                "Host": "unix:///var/run/docker.sock",
                "SkipTLSVerify": false
                }
            }
        }
        """

    @classmethod
    def contexts(cls) -> Sequence[Context]:
        """Context list.
        Returns:
            (Context): List of context objects.
        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    @classmethod
    def get_current_context(cls) -> Context:
        """Get current context.
        Returns:
            (Context): current context object.
        """

    @classmethod
    def set_current_context(cls, name: str = "default") -> None: ...
    @classmethod
    def remove_context(cls, name: str) -> None:
        """Remove a context. Similar to the ``docker context rm`` command.

        Args:
            name (str): The name of the context

        Raises:
            :py:class:`docker.errors.MissingContextParameter`
                If a context name is not provided.
            :py:class:`docker.errors.ContextNotFound`
                If a context with the name does not exist.
            :py:class:`docker.errors.ContextException`
                If name is default.

        Example:

        >>> from docker.context import ContextAPI
        >>> ContextAPI.remove_context(name='test')
        >>>
        """

    @classmethod
    def inspect_context(cls, name: str = "default") -> Context:
        """Remove a context. Similar to the ``docker context inspect`` command.

        Args:
            name (str): The name of the context

        Raises:
            :py:class:`docker.errors.MissingContextParameter`
                If a context name is not provided.
            :py:class:`docker.errors.ContextNotFound`
                If a context with the name does not exist.

        Example:

        >>> from docker.context import ContextAPI
        >>> ContextAPI.remove_context(name='test')
        >>>
        """
