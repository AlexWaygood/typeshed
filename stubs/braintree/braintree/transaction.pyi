from _typeshed import Incomplete
from decimal import Decimal
from typing import Final

from braintree.add_on import AddOn
from braintree.address import Address
from braintree.amex_express_checkout_card import AmexExpressCheckoutCard
from braintree.android_pay_card import AndroidPayCard
from braintree.apple_pay_card import ApplePayCard
from braintree.authorization_adjustment import AuthorizationAdjustment
from braintree.credit_card import CreditCard
from braintree.customer import Customer
from braintree.descriptor import Descriptor
from braintree.disbursement_detail import DisbursementDetail
from braintree.discount import Discount
from braintree.dispute import Dispute
from braintree.europe_bank_account import EuropeBankAccount
from braintree.facilitated_details import FacilitatedDetails
from braintree.facilitator_details import FacilitatorDetails
from braintree.local_payment import LocalPayment
from braintree.masterpass_card import MasterpassCard
from braintree.meta_checkout_card import MetaCheckoutCard
from braintree.meta_checkout_token import MetaCheckoutToken
from braintree.package_details import PackageDetails
from braintree.payment_facilitator import PaymentFacilitator
from braintree.paypal_account import PayPalAccount
from braintree.paypal_here import PayPalHere
from braintree.resource import Resource
from braintree.risk_data import RiskData
from braintree.samsung_pay_card import SamsungPayCard
from braintree.sepa_direct_debit_account import SepaDirectDebitAccount
from braintree.status_event import StatusEvent
from braintree.subscription_details import SubscriptionDetails
from braintree.three_d_secure_info import ThreeDSecureInfo
from braintree.us_bank_account import UsBankAccount
from braintree.venmo_account import VenmoAccount
from braintree.visa_checkout_card import VisaCheckoutCard

class Transaction(Resource):
    """
    A class representing Braintree Transaction objects.

    An example of creating a sale transaction with all available fields::

        result = Transaction.sale({
            "amount": "100.00",
            "order_id": "123",
            "channel": "MyShoppingCartProvider",
            "credit_card": {
                "number": "5105105105105100",
                "expiration_date": "05/2011",
                "cvv": "123"
            },
            "customer": {
                "first_name": "Dan",
                "last_name": "Smith",
                "company": "Braintree",
                "email": "dan@example.com",
                "phone": "419-555-1234",
                "fax": "419-555-1235",
                "website": "https://www.braintreepayments.com"
            },
            "billing": {
                "company": "Braintree",
                "country_name": "United States of America",
                "extended_address": "Suite 403",
                "first_name": "Carl",
                "international_phone": { "country_code": "1", "national_number": "3121234567" },
                "last_name": "Jones",
                "locality": "Chicago",
                "phone_number": "312-123-4567",
                "postal_code": "60622",
                "region": "IL",
                "street_address": "123 E Main St"
            },
            "shipping": {
                "company": "Braintree",
                "country_name": "United States of America",
                "extended_address": "Apt 2F",
                "first_name": "Andrew",
                "international_phone": { "country_code": "1", "national_number": "3121234567" },
                "last_name": "Mason",
                "locality": "Bartlett",
                "phone_number": "312-123-4567",
                "postal_code": "60103",
                "region": "IL",
                "street_address": "456 W Main St"
            }
        })

        print(result.transaction.amount)
        print(result.transaction.order_id)

    For more information on Transactions, see https://developer.paypal.com/braintree/docs/reference/request/transaction/sale/python

    """

    class CreatedUsing:
        """
        Constants representing how the transaction was created.  Available types are:

        * braintree.Transaction.CreatedUsing.FullInformation
        * braintree.Transaction.CreatedUsing.Token
        """

        FullInformation: Final = "full_information"
        Token: Final = "token"

    class GatewayRejectionReason:
        """
        Constants representing gateway rejection reasons. Available types are:

        * braintree.Transaction.GatewayRejectionReason.Avs
        * braintree.Transaction.GatewayRejectionReason.AvsAndCvv
        * braintree.Transaction.GatewayRejectionReason.Cvv
        * braintree.Transaction.GatewayRejectionReason.Duplicate
        * braintree.Transaction.GatewayRejectionReason.ExcessiveRetry
        * braintree.Transaction.GatewayRejectionReason.Fraud
        * braintree.Transaction.GatewayRejectionReason.RiskThreshold
        * braintree.Transaction.GatewayRejectionReason.ThreeDSecure
        * braintree.Transaction.GatewayRejectionReason.TokenIssuance
        """

        ApplicationIncomplete: Final = "application_incomplete"
        Avs: Final = "avs"
        AvsAndCvv: Final = "avs_and_cvv"
        Cvv: Final = "cvv"
        Duplicate: Final = "duplicate"
        ExcessiveRetry: Final = "excessive_retry"
        Fraud: Final = "fraud"
        RiskThreshold: Final = "risk_threshold"
        ThreeDSecure: Final = "three_d_secure"
        TokenIssuance: Final = "token_issuance"

    class ReasonCode:
        ANY_REASON_CODE: Final = "any_reason_code"

    class Source:
        Api: Final = "api"
        ControlPanel: Final = "control_panel"
        Recurring: Final = "recurring"

    class Status:
        """
        Constants representing transaction statuses. Available statuses are:

        * braintree.Transaction.Status.AuthorizationExpired
        * braintree.Transaction.Status.Authorized
        * braintree.Transaction.Status.Authorizing
        * braintree.Transaction.Status.SettlementPending
        * braintree.Transaction.Status.SettlementDeclined
        * braintree.Transaction.Status.Failed
        * braintree.Transaction.Status.GatewayRejected
        * braintree.Transaction.Status.ProcessorDeclined
        * braintree.Transaction.Status.Settled
        * braintree.Transaction.Status.Settling
        * braintree.Transaction.Status.SubmittedForSettlement
        * braintree.Transaction.Status.Voided
        """

        AuthorizationExpired: Final = "authorization_expired"
        Authorized: Final = "authorized"
        Authorizing: Final = "authorizing"
        Failed: Final = "failed"
        GatewayRejected: Final = "gateway_rejected"
        ProcessorDeclined: Final = "processor_declined"
        Settled: Final = "settled"
        SettlementConfirmed: Final = "settlement_confirmed"
        SettlementDeclined: Final = "settlement_declined"
        SettlementFailed: Final = "settlement_failed"
        SettlementPending: Final = "settlement_pending"
        Settling: Final = "settling"
        SubmittedForSettlement: Final = "submitted_for_settlement"
        Voided: Final = "voided"

    class Type:
        """
        Constants representing transaction types. Available types are:

        * braintree.Transaction.Type.Credit
        * braintree.Transaction.Type.Sale
        """

        Credit: Final = "credit"
        Sale: Final = "sale"

    class IndustryType:
        Lodging: Final = "lodging"
        TravelAndCruise: Final = "travel_cruise"
        TravelAndFlight: Final = "travel_flight"

    class AdditionalCharge:
        Restaurant: Final = "restaurant"
        GiftShop: Final = "gift_shop"
        MiniBar: Final = "mini_bar"
        Telephone: Final = "telephone"
        Laundry: Final = "laundry"
        Other: Final = "other"

    @staticmethod
    def adjust_authorization(transaction_id, amount):
        """
        adjust authorization for an existing transaction.

        It expects a `transaction_id` and `amount`, which is the new total authorization amount

        result = braintree.Transaction.adjust_authorization("my_transaction_id", "amount")

        """

    @staticmethod
    def clone_transaction(transaction_id, params): ...
    @staticmethod
    def credit(params=None):
        """
        Creates a transaction of type Credit.

        Amount is required. Also, a credit card,
        customer_id or payment_method_token is required. ::

            result = braintree.Transaction.credit({
                "amount": "100.00",
                "payment_method_token": "my_token"
            })

            result = braintree.Transaction.credit({
                "amount": "100.00",
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "12/2012"
                }
            })

            result = braintree.Transaction.credit({
                "amount": "100.00",
                "customer_id": "my_customer_id"
            })

        """

    @staticmethod
    def find(transaction_id):
        """
        Find a transaction, given a transaction_id. This does not return
        a result object. This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>` if the provided
        credit_card_id is not found. ::

            transaction = braintree.Transaction.find("my_transaction_id")
        """

    @staticmethod
    def refund(transaction_id, amount_or_options=None):
        """
        Refunds an existing transaction.

        It expects a transaction_id.::

            result = braintree.Transaction.refund("my_transaction_id")

        """

    @staticmethod
    def sale(params=None):
        """
        Creates a transaction of type Sale. Amount is required. Also, a credit card,
        customer_id or payment_method_token is required. ::

            result = braintree.Transaction.sale({
                "amount": "100.00",
                "payment_method_token": "my_token"
            })

            result = braintree.Transaction.sale({
                "amount": "100.00",
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "12/2012"
                }
            })

            result = braintree.Transaction.sale({
                "amount": "100.00",
                "customer_id": "my_customer_id"
            })
        """

    @staticmethod
    def search(*query): ...
    @staticmethod
    def submit_for_settlement(transaction_id, amount=None, params=None):
        """
        Submits an authorized transaction for settlement.

        Requires the transaction id::

            result = braintree.Transaction.submit_for_settlement("my_transaction_id")

        """

    @staticmethod
    def update_details(transaction_id, params=None):
        """
        Updates existing details for transaction submitted_for_settlement.

        Requires the transaction id::

            result = braintree.Transaction.update_details("my_transaction_id", {
                "amount": "100.00",
                "order_id": "123",
                "descriptor": {
                    "name": "123*123456789012345678",
                    "phone": "3334445555",
                    "url": "url.com"
                }
            )

        """

    @staticmethod
    def void(transaction_id):
        """
        Voids an existing transaction.

        It expects a transaction_id.::

            result = braintree.Transaction.void("my_transaction_id")

        """

    @staticmethod
    def create(params):
        """
        Creates a transaction. Amount and type are required. Also, a credit card,
        customer_id or payment_method_token is required. ::

            result = braintree.Transaction.sale({
                "type": braintree.Transaction.Type.Sale,
                "amount": "100.00",
                "payment_method_token": "my_token"
            })

            result = braintree.Transaction.sale({
                "type": braintree.Transaction.Type.Sale,
                "amount": "100.00",
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "12/2012"
                }
            })

            result = braintree.Transaction.sale({
                "type": braintree.Transaction.Type.Sale,
                "amount": "100.00",
                "customer_id": "my_customer_id"
            })
        """

    @staticmethod
    def clone_signature(): ...
    @staticmethod
    def create_signature(): ...
    @staticmethod
    def submit_for_settlement_signature(): ...
    @staticmethod
    def submit_for_partial_settlement_signature(): ...
    @staticmethod
    def package_tracking_signature(): ...
    @staticmethod
    def package_tracking(transaction_id, params=None):
        """
        Creates a request to send package tracking information for a transaction which has already submitted for settlement.

        Requires the transaction id of the transaction and the package tracking request details::

            result = braintree.Transaction.package_tracking("my_transaction_id", params )

        """

    @staticmethod
    def update_details_signature(): ...
    @staticmethod
    def refund_signature(): ...
    @staticmethod
    def submit_for_partial_settlement(transaction_id, amount, params=None):
        """
        Creates a partial settlement transaction for an authorized transaction

        Requires the transaction id of the authorized transaction and an amount::

            result = braintree.Transaction.submit_for_partial_settlement("my_transaction_id", "20.00")

        """
    amount: Decimal
    tax_amount: Decimal | None
    discount_amount: Decimal | None
    shipping_amount: Decimal | None
    billing_details: Address
    credit_card_details: CreditCard
    packages: list[PackageDetails]
    paypal_details: PayPalAccount
    paypal_here_details: PayPalHere
    local_payment_details: LocalPayment
    sepa_direct_debit_account_details: SepaDirectDebitAccount
    europe_bank_account_details: EuropeBankAccount
    us_bank_account: UsBankAccount
    apple_pay_details: ApplePayCard
    android_pay_card_details: AndroidPayCard
    amex_express_checkout_card_details: AmexExpressCheckoutCard
    venmo_account_details: VenmoAccount
    visa_checkout_card_details: VisaCheckoutCard
    masterpass_card_details: MasterpassCard
    samsung_pay_card_details: SamsungPayCard
    meta_checkout_card_details: MetaCheckoutCard
    meta_checkout_token_details: MetaCheckoutToken
    sca_exemption_requested: Incomplete
    customer_details: Customer
    shipping_details: Address
    add_ons: list[AddOn]
    discounts: list[Discount]
    status_history: list[StatusEvent]
    subscription_details: SubscriptionDetails
    descriptor: Descriptor
    disbursement_details: DisbursementDetail
    disputes: list[Dispute]
    authorization_adjustments: list[AuthorizationAdjustment]
    payment_instrument_type: Incomplete
    risk_data: RiskData | None
    three_d_secure_info: ThreeDSecureInfo | None
    facilitated_details: FacilitatedDetails
    facilitator_details: FacilitatorDetails
    network_transaction_id: Incomplete
    payment_facilitator: PaymentFacilitator
    def __init__(self, gateway, attributes) -> None: ...
    @property
    def vault_billing_address(self):
        """
        The vault billing address associated with this transaction
        """

    @property
    def vault_credit_card(self):
        """
        The vault credit card associated with this transaction
        """

    @property
    def vault_customer(self):
        """
        The vault customer associated with this transaction
        """

    @property
    def is_disbursed(self): ...
    @property
    def line_items(self):
        """
        The line items associated with this transaction
        """
