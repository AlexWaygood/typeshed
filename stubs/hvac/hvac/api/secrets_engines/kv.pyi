"""Kv secret backend methods module."""

from _typeshed import Incomplete

from hvac.api.vault_api_base import VaultApiBase

logger: Incomplete

class Kv(VaultApiBase):
    """Class containing methods for the key/value secrets_engines backend API routes.
    Reference: https://www.vaultproject.io/docs/secrets/kv/index.html

    """

    allowed_kv_versions: Incomplete
    def __init__(self, adapter, default_kv_version: str = "2") -> None:
        """Create a new Kv instance.

        :param adapter: Instance of :py:class:`hvac.adapters.Adapter`; used for performing HTTP requests.
        :type adapter: hvac.adapters.Adapter
        :param default_kv_version: KV version number (e.g., '1') to use as the default when accessing attributes/methods
            under this class.
        :type default_kv_version: str | unicode
        """

    @property
    def v1(self):
        """Accessor for kv version 1 class / method. Provided via the :py:class:`hvac.api.secrets_engines.kv_v1.KvV1` class.

        :return: This Kv instance's associated KvV1 instance.
        :rtype: hvac.api.secrets_engines.kv_v1.KvV1
        """

    @property
    def v2(self):
        """Accessor for kv version 2 class / method. Provided via the :py:class:`hvac.api.secrets_engines.kv_v2.KvV2` class.

        :return: This Kv instance's associated KvV2 instance.
        :rtype: hvac.api.secrets_engines.kv_v2.KvV2
        """

    @property
    def default_kv_version(self): ...
    @default_kv_version.setter
    def default_kv_version(self, default_kv_version) -> None: ...
    def __getattr__(self, item):
        """Overridden magic method used to direct method calls to the appropriate KV version's hvac class.

        :param item: Name of the attribute/method being accessed
        :type item: str | unicode
        :return: The selected secrets_engines class corresponding to this instance's default_kv_version setting
        :rtype: hvac.api.vault_api_base.VaultApiBase
        """
