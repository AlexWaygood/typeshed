from typing import Final

class TransactionAmounts:
    """A class of constants for transaction amounts that will cause different statuses."""

    Authorize: Final = "1000.00"
    Decline: Final = "2000.00"
    HardDecline: Final = "2015.00"
    Fail: Final = "3000.00"
