from collections.abc import Iterable
from typing import Any

from docker.types import DriverConfig

class SecretApiMixin:
    def create_secret(
        self, name: str, data: bytes, labels: dict[str, Any] | None = None, driver: DriverConfig | None = None
    ) -> dict[str, Any]:
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

    def inspect_secret(self, id: str) -> dict[str, Any]:
        """
        Retrieve secret metadata

        Args:
            id (string): Full ID of the secret to inspect

        Returns (dict): A dictionary of metadata

        Raises:
            :py:class:`docker.errors.NotFound`
                if no secret with that ID exists
        """

    def remove_secret(self, id: str) -> bool:
        """
        Remove a secret

        Args:
            id (string): Full ID of the secret to remove

        Returns (boolean): True if successful

        Raises:
            :py:class:`docker.errors.NotFound`
                if no secret with that ID exists
        """

    def secrets(self, filters: dict[str, Any] | None = None) -> Iterable[dict[str, Any]]:
        """
        List secrets

        Args:
            filters (dict): A map of filters to process on the secrets
            list. Available filters: ``names``

        Returns (list): A list of secrets
        """
