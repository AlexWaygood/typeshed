from _typeshed import Incomplete
from collections.abc import Generator

from .resource import Collection, Model

class Plugin(Model):
    """
    A plugin on the server.
    """

    @property
    def name(self):
        """
        The plugin's name.
        """

    @property
    def enabled(self):
        """
        Whether the plugin is enabled.
        """

    @property
    def settings(self):
        """
        A dictionary representing the plugin's configuration.
        """

    def configure(self, options) -> None:
        """
        Update the plugin's settings.

        Args:
            options (dict): A key-value mapping of options.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def disable(self, force: bool = False) -> None:
        """
        Disable the plugin.

        Args:
            force (bool): Force disable. Default: False

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def enable(self, timeout: int = 0) -> None:
        """
        Enable the plugin.

        Args:
            timeout (int): Timeout in seconds. Default: 0

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def push(self):
        """
        Push the plugin to a remote registry.

        Returns:
            A dict iterator streaming the status of the upload.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def remove(self, force: bool = False):
        """
        Remove the plugin from the server.

        Args:
            force (bool): Remove even if the plugin is enabled.
                Default: False

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def upgrade(self, remote=None) -> Generator[Incomplete, Incomplete, None]:
        """
        Upgrade the plugin.

        Args:
            remote (string): Remote reference to upgrade to. The
                ``:latest`` tag is optional and is the default if omitted.
                Default: this plugin's name.

        Returns:
            A generator streaming the decoded API logs
        """

class PluginCollection(Collection[Plugin]):
    model: type[Plugin]
    def create(self, name, plugin_data_dir, gzip: bool = False):  # type:ignore[override]
        """
        Create a new plugin.

        Args:
            name (string): The name of the plugin. The ``:latest`` tag is
                optional, and is the default if omitted.
            plugin_data_dir (string): Path to the plugin data directory.
                Plugin data directory must contain the ``config.json``
                manifest file and the ``rootfs`` directory.
            gzip (bool): Compress the context using gzip. Default: False

        Returns:
            (:py:class:`Plugin`): The newly created plugin.
        """

    def get(self, name):
        """
        Gets a plugin.

        Args:
            name (str): The name of the plugin.

        Returns:
            (:py:class:`Plugin`): The plugin.

        Raises:
            :py:class:`docker.errors.NotFound` If the plugin does not
            exist.
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def install(self, remote_name, local_name=None):
        """
        Pull and install a plugin.

        Args:
            remote_name (string): Remote reference for the plugin to
                install. The ``:latest`` tag is optional, and is the
                default if omitted.
            local_name (string): Local name for the pulled plugin.
                The ``:latest`` tag is optional, and is the default if
                omitted. Optional.

        Returns:
            (:py:class:`Plugin`): The installed plugin
        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def list(self):
        """
        List plugins installed on the server.

        Returns:
            (list of :py:class:`Plugin`): The plugins.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
