from _typeshed import Incomplete

from braintree.resource import Resource

class LocalPaymentFunded(Resource):
    """
    A class representing Braintree LocalPaymentFunded webhook.
    """

    transaction: Incomplete
    def __init__(self, gateway, attributes) -> None: ...
