from braintree.graphql.types.payment_options import PaymentOptions
from braintree.graphql.types.payment_recommendation import PaymentRecommendation

class CustomerRecommendations:
    """
    A union of all possible customer recommendations associated with a PayPal customer session.
    """

    payment_options: list[PaymentOptions]
    payment_recommendations: list[PaymentRecommendation]
    def __init__(self, payment_recommendations: list[PaymentRecommendation] | None = None) -> None:
        """
        Initialize customer recommendations.

        Args:
            payment_recommendations: A list of PaymentRecommendation objects
        """
