from _typeshed import Incomplete
from typing import Final

from braintree.resource import Resource
from braintree.subscription import Subscription

class ApplePayCard(Resource):
    """
    A class representing Braintree Apple Pay card objects.
    """

    class CardType:
        """
        Contants representing the type of the credit card.  Available types are:

        * Braintree.ApplePayCard.AmEx
        * Braintree.ApplePayCard.MasterCard
        * Braintree.ApplePayCard.Visa
        """

        AmEx: Final = "Apple Pay - American Express"
        MasterCard: Final = "Apple Pay - MasterCard"
        Visa: Final = "Apple Pay - Visa"

    is_expired: Incomplete
    subscriptions: list[Subscription]
    def __init__(self, gateway, attributes) -> None: ...
    @property
    def expiration_date(self): ...
    @staticmethod
    def signature() -> list[str | dict[str, list[str]]]: ...
