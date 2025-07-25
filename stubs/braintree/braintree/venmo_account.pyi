from braintree.resource import Resource
from braintree.subscription import Subscription

class VenmoAccount(Resource):
    """
    A class representing Braintree Venmo accounts.
    """

    subscriptions: list[Subscription]
    def __init__(self, gateway, attributes) -> None: ...
