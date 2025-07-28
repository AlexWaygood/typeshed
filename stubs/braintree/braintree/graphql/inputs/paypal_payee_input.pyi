from _typeshed import Incomplete
from typing_extensions import Self

class PayPalPayeeInput:
    """
    The details for the merchant who receives the funds and fulfills the order.
    The merchant is also known as the payee.
    """

    def __init__(self, email_address: str | None = None, client_id: str | None = None) -> None: ...
    def to_graphql_variables(self) -> dict[str, Incomplete]:
        """
        Returns a dictionary representing the input object, to pass as variables to a GraphQL mutation.
        """

    @staticmethod
    def builder() -> Builder:
        """
        Creates a builder instance for fluent construction of PayPalPayeeInput objects.
        """

    class Builder:
        def __init__(self) -> None: ...
        def email_address(self, email_address: str) -> Self:
            """
            Sets the email address of this merchant.
            """

        def client_id(self, client_id: str) -> Self:
            """
            Sets the public ID for the payee- or merchant-created app.
            """

        def build(self) -> PayPalPayeeInput: ...
