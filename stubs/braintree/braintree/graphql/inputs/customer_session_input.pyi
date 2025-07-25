from _typeshed import Incomplete
from typing_extensions import Self

from braintree.graphql.inputs.phone_input import PhoneInput

class CustomerSessionInput:
    """
    Customer identifying information for a PayPal customer session.
    """

    def __init__(
        self,
        email: str | None = None,
        hashed_email: str | None = None,
        phone: PhoneInput | None = None,
        hashed_phone_number: str | None = None,
        device_fingerprint_id: str | None = None,
        paypal_app_installed: bool | None = None,
        venmo_app_installed: bool | None = None,
        user_agent: str | None = None,
    ) -> None: ...
    def to_graphql_variables(self) -> dict[str, Incomplete]: ...
    @staticmethod
    def builder() -> Builder:
        """
        Creates a builder instance for fluent construction of CustomerSessionInput objects.
        """

    class Builder:
        def __init__(self) -> None: ...
        def email(self, email: str) -> Self:
            """
            Sets the customer email address.
            """

        def hashed_email(self, hashed_email: str) -> Self:
            """
            Sets the hashed customer email address.
            """

        def phone(self, phone: PhoneInput) -> Self:
            """
            Sets the customer phone number input object.
            """

        def hashed_phone_number(self, hashed_phone_number: str) -> Self:
            """
            Sets the hashed customer phone number
            """

        def device_fingerprint_id(self, device_fingerprint_id: str) -> Self:
            """
            Sets the device fingerprint ID.
            """

        def paypal_app_installed(self, paypal_app_installed: bool) -> Self:
            """
            Sets whether the PayPal app is installed on the customer's device.
            """

        def venmo_app_installed(self, venmo_app_installed: bool) -> Self:
            """
            Sets whether the Venmo app is installed on the customer's device.
            """

        def user_agent(self, user_agent: str) -> Self:
            """
            Sets user agent from the request originating from the customer's device.
            This will be used to identify the customer's operating system and browser versions.
            """

        def build(self) -> CustomerSessionInput: ...
