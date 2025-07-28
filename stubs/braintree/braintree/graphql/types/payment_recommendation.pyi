from braintree.graphql.enums import RecommendedPaymentOption

class PaymentRecommendation:
    """
    Represents a single  payment method and priority associated with a PayPal customer session.
    """

    payment_option: RecommendedPaymentOption
    recommended_priority: int
    def __init__(self, payment_option: RecommendedPaymentOption, recommended_priority: int) -> None: ...
