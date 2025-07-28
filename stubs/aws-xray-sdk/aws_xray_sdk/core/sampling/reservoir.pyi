from enum import Enum

class Reservoir:
    """
    Centralized thread-safe reservoir which holds fixed sampling
    quota, borrowed count and TTL.
    """

    def __init__(self) -> None: ...
    def borrow_or_take(self, now: int, can_borrow: bool | None) -> ReservoirDecision | None:
        """
        Decide whether to borrow or take one quota from
        the reservoir. Return ``False`` if it can neither
        borrow nor take. This method is thread-safe.
        """

    def load_quota(self, quota: int | None, TTL: int | None, interval: int | None) -> None:
        """
        Load new quota with a TTL. If the input is None,
        the reservoir will continue using old quota until it
        expires or has a non-None quota/TTL in a future load.
        """

    @property
    def quota(self) -> int | None: ...
    @property
    def TTL(self) -> int | None: ...

class ReservoirDecision(Enum):
    """
    An Enum of decisions the reservoir could make based on
    assigned quota with TTL and the current timestamp/usage.
    """

    TAKE = "take"
    BORROW = "borrow"
    NO = "no"
