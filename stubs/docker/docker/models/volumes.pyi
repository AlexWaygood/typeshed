from typing import Any

from .resource import Collection, Model

class Volume(Model):
    """A volume."""

    id_attribute: str
    @property
    def name(self) -> str:
        """The name of the volume."""

    def remove(self, force: bool = False) -> None:
        """
        Remove this volume.

        Args:
            force (bool): Force removal of volumes that were already removed
                out of band by the volume driver plugin.
        Raises:
            :py:class:`docker.errors.APIError`
                If volume failed to remove.
        """

class VolumeCollection(Collection[Volume]):
    """Volumes on the Docker server."""

    model: type[Volume]
    def create(self, name: str | None = None, **kwargs) -> Volume:  # type:ignore[override]
        """
        Create a volume.

        Args:
            name (str): Name of the volume.  If not specified, the engine
                generates a name.
            driver (str): Name of the driver used to create the volume
            driver_opts (dict): Driver options as a key-value dictionary
            labels (dict): Labels to set on the volume

        Returns:
            (:py:class:`Volume`): The volume created.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.

        Example:

            >>> volume = client.volumes.create(name='foobar', driver='local',
                    driver_opts={'foo': 'bar', 'baz': 'false'},
                    labels={"key": "value"})

        """

    def get(self, volume_id: str) -> Volume:
        """
        Get a volume.

        Args:
            volume_id (str): Volume name.

        Returns:
            (:py:class:`Volume`): The volume.

        Raises:
            :py:class:`docker.errors.NotFound`
                If the volume does not exist.
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def list(self, **kwargs) -> list[Volume]:
        """
        List volumes. Similar to the ``docker volume ls`` command.

        Args:
            filters (dict): Server-side list filtering options.

        Returns:
            (list of :py:class:`Volume`): The volumes.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """

    def prune(self, filters: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Delete unused volumes

        Args:
            filters (dict): Filters to process on the prune list.

        Returns:
            (dict): A dict containing a list of deleted volume names and
                the amount of disk space reclaimed in bytes.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
