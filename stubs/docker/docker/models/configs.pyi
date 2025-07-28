from .resource import Collection, Model

class Config(Model):
    """A config."""

    id_attribute: str
    @property
    def name(self) -> str: ...
    def remove(self) -> bool:
        """
        Remove this config.

        Raises:
            :py:class:`docker.errors.APIError`
                If config failed to remove.
        """

class ConfigCollection(Collection[Config]):
    """Configs on the Docker server."""

    model: type[Config]
    def create(self, **kwargs) -> Config:  # type:ignore[override]
        """
        Create a config

        Args:
            name (string): Name of the config
            data (bytes): Config data to be stored
            labels (dict): A mapping of labels to assign to the config
            templating (dict): dictionary containing the name of the
                               templating driver to be used expressed as
                               { name: <templating_driver_name>}

        Returns (dict): ID of the newly created config
        """

    def get(self, config_id: str) -> Config:
        """
        Get a config.

        Args:
            config_id (str): Config ID.

        Returns:
            (:py:class:`Config`): The config.

        Raises:
            :py:class:`docker.errors.NotFound`
                If the config does not exist.
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def list(self, **kwargs) -> list[Config]:
        """
        List configs. Similar to the ``docker config ls`` command.

        Args:
            filters (dict): Server-side list filtering options.

        Returns:
            (list of :py:class:`Config`): The configs.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
