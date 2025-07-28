from _typeshed import Incomplete

from braintree.address import Address
from braintree.amex_express_checkout_card import AmexExpressCheckoutCard
from braintree.android_pay_card import AndroidPayCard
from braintree.apple_pay_card import ApplePayCard
from braintree.credit_card import CreditCard
from braintree.error_result import ErrorResult
from braintree.europe_bank_account import EuropeBankAccount
from braintree.masterpass_card import MasterpassCard
from braintree.paypal_account import PayPalAccount
from braintree.resource import Resource
from braintree.resource_collection import ResourceCollection
from braintree.samsung_pay_card import SamsungPayCard
from braintree.successful_result import SuccessfulResult
from braintree.us_bank_account import UsBankAccount
from braintree.venmo_account import VenmoAccount
from braintree.visa_checkout_card import VisaCheckoutCard

class Customer(Resource):
    """
    A class representing a customer.

    An example of creating an customer with all available fields::

        result = braintree.Customer.create({
            "company": "Some company",
            "credit_card": {
                "billing_address": {
                    "company": "Braintree",
                    "country_name": "United States of America",
                    "extended_address": "Unit 1",
                    "first_name": "John",
                    "international_phone": { "country_code": "1", "national_number": "3121234567" },
                    "last_name": "Doe",
                    "locality": "Chicago",
                    "phone_number": "312-123-4567",
                    "postal_code": "60606",
                    "region": "IL",
                    "street_address": "111 First Street"
                },
                "cardholder_name": "John Doe",
                "cvv": "123",
                "expiration_date": "12/2012",
                "number": "4111111111111111",
                "options": {
                    "verification_amount": "2.00",
                    "verify_card": True
                },
                "token": "my_token"
            },
            "custom_fields": {
                "my_key": "some value"
            },
            "email": "john.doe@example.com",
            "fax": "123-555-1212",
            "first_name": "John",
            "id": "my_customer_id",
            "international_phone": { "country_code": "1", "national_number": "3121234567" },
            "last_name": "Doe",
            "phone": "123-555-1221",
            "website": "http://www.example.com"
        })

        print(result.customer.id)
        print(result.customer.first_name)

    For more information on Customers, see https://developer.paypal.com/braintree/docs/reference/request/customer/create/python

    """

    @staticmethod
    def all() -> ResourceCollection:
        """Return a collection of all customers."""

    @staticmethod
    def create(params: dict[str, Incomplete] | None = None) -> SuccessfulResult | ErrorResult | None:
        """
        Create a Customer

        No field is required::

            result = braintree.Customer.create({
                "company": "Some company",
                "first_name": "John"
            })

        """

    @staticmethod
    def delete(customer_id: str) -> SuccessfulResult:
        """
        Delete a customer

        Given a customer_id::

            result = braintree.Customer.delete("my_customer_id")

        """

    @staticmethod
    def find(customer_id: str, association_filter_id: str | None = None) -> Customer:
        """
        Find an customer, given a customer_id.  This does not return a result
        object.  This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>` if the provided customer_id
        is not found. ::

            customer = braintree.Customer.find("my_customer_id")
        """

    @staticmethod
    def search(*query) -> ResourceCollection: ...
    @staticmethod
    def update(customer_id: str, params: dict[str, Incomplete] | None = None) -> SuccessfulResult | ErrorResult | None:
        """
        Update an existing Customer

        By customer_id. The params are similar to create::

            result = braintree.Customer.update("my_customer_id", {
                "last_name": "Smith"
            })

        """

    @staticmethod
    def create_signature() -> (
        list[
            str
            | dict[str, list[str]]
            | dict[str, list[str | dict[str, list[str]] | dict[str, list[str | dict[str, list[str]]]]]]
            | dict[str, list[str | dict[str, list[str]]]]
            | dict[str, list[dict[str, list[str | dict[str, list[str | dict[str, list[str]]]]]]]]
        ]
    ): ...
    @staticmethod
    def update_signature() -> (
        list[
            str
            | dict[str, list[str]]
            | dict[str, list[str | dict[str, list[str]] | dict[str, list[str | dict[str, list[str]]]]]]
            | dict[str, list[str | dict[str, list[str]]]]
            | dict[str, list[dict[str, list[str | dict[str, list[str | dict[str, list[str]]]]]]]]
        ]
    ): ...
    payment_methods: list[Resource]
    credit_cards: list[CreditCard]
    addresses: list[Address]
    paypal_accounts: list[PayPalAccount]
    apple_pay_cards: list[ApplePayCard]
    android_pay_cards: list[AndroidPayCard]
    amex_express_checkout_cards: list[AmexExpressCheckoutCard]
    europe_bank_accounts: list[EuropeBankAccount]
    venmo_accounts: list[VenmoAccount]
    us_bank_accounts: list[UsBankAccount]
    visa_checkout_cards: list[VisaCheckoutCard]
    masterpass_cards: list[MasterpassCard]
    samsung_pay_cards: list[SamsungPayCard]
    def __init__(self, gateway, attributes) -> None: ...
