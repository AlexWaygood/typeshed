class PluginApiMixin:
    def configure_plugin(self, name, options):
        """
        Configure a plugin.

        Args:
            name (string): The name of the plugin. The ``:latest`` tag is
                optional, and is the default if omitted.
            options (dict): A key-value mapping of options

        Returns:
            ``True`` if successful
        """

    def create_plugin(self, name, plugin_data_dir, gzip: bool = False):
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
            ``True`` if successful
        """

    def disable_plugin(self, name, force: bool = False):
        """
        Disable an installed plugin.

        Args:
            name (string): The name of the plugin. The ``:latest`` tag is
                optional, and is the default if omitted.
            force (bool): To enable the force query parameter.

        Returns:
            ``True`` if successful
        """

    def enable_plugin(self, name, timeout: int = 0):
        """
        Enable an installed plugin.

        Args:
            name (string): The name of the plugin. The ``:latest`` tag is
                optional, and is the default if omitted.
            timeout (int): Operation timeout (in seconds). Default: 0

        Returns:
            ``True`` if successful
        """

    def inspect_plugin(self, name):
        """
        Retrieve plugin metadata.

        Args:
            name (string): The name of the plugin. The ``:latest`` tag is
                optional, and is the default if omitted.

        Returns:
            A dict containing plugin info
        """

    def pull_plugin(self, remote, privileges, name=None):
        """
        Pull and install a plugin. After the plugin is installed, it can be
        enabled using :py:meth:`~enable_plugin`.

        Args:
            remote (string): Remote reference for the plugin to install.
                The ``:latest`` tag is optional, and is the default if
                omitted.
            privileges (:py:class:`list`): A list of privileges the user
                consents to grant to the plugin. Can be retrieved using
                :py:meth:`~plugin_privileges`.
            name (string): Local name for the pulled plugin. The
                ``:latest`` tag is optional, and is the default if omitted.

        Returns:
            An iterable object streaming the decoded API logs
        """

    def plugins(self):
        """
        Retrieve a list of installed plugins.

        Returns:
            A list of dicts, one per plugin
        """

    def plugin_privileges(self, name):
        """
        Retrieve list of privileges to be granted to a plugin.

        Args:
            name (string): Name of the remote plugin to examine. The
                ``:latest`` tag is optional, and is the default if omitted.

        Returns:
            A list of dictionaries representing the plugin's
            permissions

        """

    def push_plugin(self, name):
        """
        Push a plugin to the registry.

        Args:
            name (string): Name of the plugin to upload. The ``:latest``
                tag is optional, and is the default if omitted.

        Returns:
            ``True`` if successful
        """

    def remove_plugin(self, name, force: bool = False):
        """
        Remove an installed plugin.

        Args:
            name (string): Name of the plugin to remove. The ``:latest``
                tag is optional, and is the default if omitted.
            force (bool): Disable the plugin before removing. This may
                result in issues if the plugin is in use by a container.

        Returns:
            ``True`` if successful
        """

    def upgrade_plugin(self, name, remote, privileges):
        """
        Upgrade an installed plugin.

        Args:
            name (string): Name of the plugin to upgrade. The ``:latest``
                tag is optional and is the default if omitted.
            remote (string): Remote reference to upgrade to. The
                ``:latest`` tag is optional and is the default if omitted.
            privileges (:py:class:`list`): A list of privileges the user
                consents to grant to the plugin. Can be retrieved using
                :py:meth:`~plugin_privileges`.

        Returns:
            An iterable object streaming the decoded API logs
        """
