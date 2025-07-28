from _typeshed import Incomplete
from typing_extensions import Self

from braintree.graphql.inputs.monetary_amount_input import MonetaryAmountInput
from braintree.graphql.inputs.paypal_payee_input import PayPalPayeeInput

class PayPalPurchaseUnitInput:
    """
    Payee and Amount of the item purchased.
    """

    def __init__(self, amount: MonetaryAmountInput | None = None, payee: PayPalPayeeInput | None = None) -> None: ...
    def to_graphql_variables(self) -> dict[str, Incomplete]:
        """
        Returns a dictionary representing the input object, to pass as variables to a GraphQL mutation.
        """

    @staticmethod
    def builder(amount: MonetaryAmountInput) -> Builder:
        """
        Creates a builder instance for fluent construction of PayPalPurchaseUnit objects.

        Args:
        amount (MonetaryAmountInput): The total order amount. The amount must be a positive number.

        """

    class Builder:
        def __init__(self, amount: MonetaryAmountInput) -> None: ...
        def payee(self, payee: PayPalPayeeInput) -> Self:
            """
            Sets the PayPal payee.
            """

        def build(self) -> PayPalPurchaseUnitInput: ...
