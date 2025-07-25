from braintree.resource import Resource

class LocalPaymentExpired(Resource):
    """
    A class representing Braintree LocalPaymentExpired webhook.
    """

    def __init__(self, gateway, attributes) -> None: ...
