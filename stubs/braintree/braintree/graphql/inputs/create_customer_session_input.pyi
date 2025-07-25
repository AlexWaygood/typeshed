from _typeshed import Incomplete
from typing_extensions import Self

from braintree.graphql.inputs.customer_session_input import CustomerSessionInput
from braintree.graphql.inputs.paypal_purchase_unit_input import PayPalPurchaseUnitInput

class CreateCustomerSessionInput:
    """
    Represents the input to request the creation of a PayPal customer session.
    """

    def __init__(
        self,
        merchant_account_id: str | None = None,
        session_id: str | None = None,
        customer: CustomerSessionInput | None = None,
        domain: str | None = None,
        purchase_units: list[PayPalPurchaseUnitInput] | None = None,
    ) -> None: ...
    def to_graphql_variables(self) -> dict[str, Incomplete]: ...
    @staticmethod
    def builder() -> Builder:
        """
        Creates a builder instance for fluent construction of CreateCustomerSessionInput objects.
        """

    class Builder:
        def __init__(self) -> None: ...
        def merchant_account_id(self, merchant_account_id: str) -> Self:
            """
            Sets the merchant account ID.
            """

        def session_id(self, session_id: str) -> Self:
            """
            Sets the customer session ID.
            """

        def customer(self, customer: CustomerSessionInput) -> Self:
            """
            Sets the input object representing customer information relevant to the customer session.
            """

        def purchase_units(self, purchase_units: list[PayPalPurchaseUnitInput]) -> Self:
            """
            Sets the Purchase Units for the items purchased.
            """

        def domain(self, domain: str) -> Self:
            """
            Sets the customer domain.
            """

        def build(self) -> CreateCustomerSessionInput: ...
