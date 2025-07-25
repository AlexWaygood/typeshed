from .resource import Collection, Model

class Secret(Model):
    """A secret."""

    id_attribute: str
    @property
    def name(self): ...
    def remove(self):
        """
        Remove this secret.

        Raises:
            :py:class:`docker.errors.APIError`
                If secret failed to remove.
        """

class SecretCollection(Collection[Secret]):
    """Secrets on the Docker server."""

    model: type[Secret]
    def create(self, **kwargs):  # type: ignore[override]
        """
        Create a secret

        Args:
            name (string): Name of the secret
            data (bytes): Secret data to be stored
            labels (dict): A mapping of labels to assign to the secret
            driver (DriverConfig): A custom driver configuration. If
                unspecified, the default ``internal`` driver will be used

        Returns (dict): ID of the newly created secret
        """

    def get(self, secret_id):
        """
        Get a secret.

        Args:
            secret_id (str): Secret ID.

        Returns:
            (:py:class:`Secret`): The secret.

        Raises:
            :py:class:`docker.errors.NotFound`
                If the secret does not exist.
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def list(self, **kwargs):
        """
        List secrets. Similar to the ``docker secret ls`` command.

        Args:
            filters (dict): Server-side list filtering options.

        Returns:
            (list of :py:class:`Secret`): The secrets.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
