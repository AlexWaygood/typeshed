import asyncio
from re import Pattern
from typing import Any, ClassVar, overload
from typing_extensions import TypeAlias, deprecated

class ChannelLayerManager:
    """
    Takes a settings dictionary of backends and initialises them on request.
    """

    backends: dict[str, BaseChannelLayer]

    def __init__(self) -> None: ...
    @property
    def configs(self) -> dict[str, Any]: ...
    def make_backend(self, name: str) -> BaseChannelLayer:
        """
        Instantiate channel layer.
        """

    def make_test_backend(self, name: str) -> Any:
        """
        Instantiate channel layer using its test config.
        """

    def __getitem__(self, key: str) -> BaseChannelLayer: ...
    def __contains__(self, key: str) -> bool: ...
    def set(self, key: str, layer: BaseChannelLayer) -> BaseChannelLayer | None:
        """
        Sets an alias to point to a new ChannelLayerWrapper instance, and
        returns the old one that it replaced. Useful for swapping out the
        backend during tests.
        """

_ChannelCapacityPattern: TypeAlias = Pattern[str] | str
_ChannelCapacityDict: TypeAlias = dict[_ChannelCapacityPattern, int]
_CompiledChannelCapacity: TypeAlias = list[tuple[Pattern[str], int]]

class BaseChannelLayer:
    """
    Base channel layer class that others can inherit from, with useful
    common functionality.
    """

    MAX_NAME_LENGTH: ClassVar[int] = 100
    expiry: int
    capacity: int
    channel_capacity: _ChannelCapacityDict
    channel_name_regex: Pattern[str]
    group_name_regex: Pattern[str]
    invalid_name_error: str

    def __init__(self, expiry: int = 60, capacity: int = 100, channel_capacity: _ChannelCapacityDict | None = None) -> None: ...
    def compile_capacities(self, channel_capacity: _ChannelCapacityDict) -> _CompiledChannelCapacity:
        """
        Takes an input channel_capacity dict and returns the compiled list
        of regexes that get_capacity will look for as self.channel_capacity
        """

    def get_capacity(self, channel: str) -> int:
        """
        Gets the correct capacity for the given channel; either the default,
        or a matching result from channel_capacity. Returns the first matching
        result; if you want to control the order of matches, use an ordered dict
        as input.
        """

    @overload
    def match_type_and_length(self, name: str) -> bool: ...
    @overload
    def match_type_and_length(self, name: object) -> bool: ...
    @overload
    def require_valid_channel_name(self, name: str, receive: bool = False) -> bool: ...
    @overload
    def require_valid_channel_name(self, name: object, receive: bool = False) -> bool: ...
    @overload
    def require_valid_group_name(self, name: str) -> bool: ...
    @overload
    def require_valid_group_name(self, name: object) -> bool: ...
    @overload
    def valid_channel_names(self, names: list[str], receive: bool = False) -> bool: ...
    @overload
    def valid_channel_names(self, names: list[Any], receive: bool = False) -> bool: ...
    def non_local_name(self, name: str) -> str:
        """
        Given a channel name, returns the "non-local" part. If the channel name
        is a process-specific channel (contains !) this means the part up to
        and including the !; if it is anything else, this means the full name.
        """

    async def send(self, channel: str, message: dict[str, Any]) -> None: ...
    async def receive(self, channel: str) -> dict[str, Any]: ...
    async def new_channel(self) -> str: ...
    async def flush(self) -> None: ...
    async def group_add(self, group: str, channel: str) -> None: ...
    async def group_discard(self, group: str, channel: str) -> None: ...
    async def group_send(self, group: str, message: dict[str, Any]) -> None: ...
    @deprecated("Use require_valid_channel_name instead.")
    def valid_channel_name(self, channel_name: str, receive: bool = False) -> bool:
        """
        Deprecated: Use require_valid_channel_name instead.
        """

    @deprecated("Use require_valid_group_name instead.")
    def valid_group_name(self, group_name: str) -> bool:
        """
        Deprecated: Use require_valid_group_name instead..
        """

_InMemoryQueueData: TypeAlias = tuple[float, dict[str, Any]]

class InMemoryChannelLayer(BaseChannelLayer):
    """
    In-memory channel layer implementation
    """

    channels: dict[str, asyncio.Queue[_InMemoryQueueData]]
    groups: dict[str, dict[str, float]]
    group_expiry: int

    def __init__(
        self,
        expiry: int = 60,
        group_expiry: int = 86400,
        capacity: int = 100,
        channel_capacity: _ChannelCapacityDict | None = ...,
    ) -> None: ...

    extensions: list[str]

    async def send(self, channel: str, message: dict[str, Any]) -> None:
        """
        Send a message onto a (general or specific) channel.
        """

    async def receive(self, channel: str) -> dict[str, Any]:
        """
        Receive the first message that arrives on the channel.
        If more than one coroutine waits on the same channel, a random one
        of the waiting coroutines will get the result.
        """

    async def new_channel(self, prefix: str = "specific.") -> str:
        """
        Returns a new channel name that can be used by something in our
        process as a specific channel.
        """

    async def flush(self) -> None: ...
    async def close(self) -> None: ...
    async def group_add(self, group: str, channel: str) -> None:
        """
        Adds the channel name to a group.
        """

    async def group_discard(self, group: str, channel: str) -> None: ...
    async def group_send(self, group: str, message: dict[str, Any]) -> None: ...

def get_channel_layer(alias: str = ...) -> BaseChannelLayer | None:
    """
    Returns a channel layer by alias, or None if it is not configured.
    """

channel_layers: ChannelLayerManager
