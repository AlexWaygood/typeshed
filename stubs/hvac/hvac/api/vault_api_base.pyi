"""Base class used by all hvac "api" classes."""

from _typeshed import Incomplete
from abc import ABCMeta
from logging import Logger

from hvac.adapters import Adapter

logger: Logger

class VaultApiBase(metaclass=ABCMeta):
    """Base class for API endpoints."""

    def __init__(self, adapter: Adapter[Incomplete]) -> None:
        """Default api class constructor.

        :param adapter: Instance of :py:class:`hvac.adapters.Adapter`; used for performing HTTP requests.
        :type adapter: hvac.adapters.Adapter
        """
