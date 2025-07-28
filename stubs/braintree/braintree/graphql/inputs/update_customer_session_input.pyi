from _typeshed import Incomplete
from typing_extensions import Self

from braintree.graphql.inputs.customer_session_input import CustomerSessionInput
from braintree.graphql.inputs.paypal_purchase_unit_input import PayPalPurchaseUnitInput

class UpdateCustomerSessionInput:
    """
    Represents the input to request an update to a PayPal customer session.
    """

    def __init__(
        self,
        session_id: str,
        customer: CustomerSessionInput | None = None,
        merchant_account_id: str | None = None,
        purchase_units: list[PayPalPurchaseUnitInput] | None = None,
    ) -> None: ...
    def to_graphql_variables(self) -> dict[str, Incomplete]: ...
    @staticmethod
    def builder(session_id: str) -> Builder:
        """
        Creates a builder instance for fluent construction of UpdateCustomerSessionInput objects.

        Args:
            session_id (str): ID of the customer session to be updated.
        """

    class Builder:
        def __init__(self, session_id: str) -> None: ...
        def merchant_account_id(self, merchant_account_id: str) -> Self:
            """
            Sets the merchant account ID.
            """

        def customer(self, customer: CustomerSessionInput) -> Self:
            """
            Sets the input object representing customer information relevant to the customer session.
            """

        def purchase_units(self, purchase_units: list[PayPalPurchaseUnitInput]) -> Self:
            """
            Sets the Purchase Units for the items purchased.
            """

        def build(self) -> UpdateCustomerSessionInput: ...
