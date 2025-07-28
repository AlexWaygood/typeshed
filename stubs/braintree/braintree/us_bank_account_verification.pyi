from typing import Final

from braintree.attribute_getter import AttributeGetter
from braintree.error_result import ErrorResult
from braintree.resource_collection import ResourceCollection
from braintree.successful_result import SuccessfulResult
from braintree.us_bank_account import UsBankAccount

class UsBankAccountVerification(AttributeGetter):
    class Status:
        """
        Constants representing transaction statuses. Available statuses are:

        * braintree.UsBankAccountVerification.Status.Failed
        * braintree.UsBankAccountVerification.Status.GatewayRejected
        * braintree.UsBankAccountVerification.Status.ProcessorDeclined
        * braintree.UsBankAccountVerification.Status.Unrecognized
        * braintree.UsBankAccountVerification.Status.Verified
        * braintree.UsBankAccountVerification.Status.Pending
        """

        Failed: Final = "failed"
        GatewayRejected: Final = "gateway_rejected"
        ProcessorDeclined: Final = "processor_declined"
        Unrecognized: Final = "unrecognized"
        Verified: Final = "verified"
        Pending: Final = "pending"

    class VerificationMethod:
        """
        Constants representing verification types. Available types are:

        * braintree.UsBankAccountVerification.VerificationMethod.NetworkCheck
        * braintree.UsBankAccountVerification.VerificationMethod.IndependentCheck
        * braintree.UsBankAccountVerification.VerificationMethod.TokenizedCheck
        * braintree.UsBankAccountVerification.VerificationMethod.MicroTransfers
        """

        NetworkCheck: Final = "network_check"
        IndependentCheck: Final = "independent_check"
        TokenizedCheck: Final = "tokenized_check"
        MicroTransfers: Final = "micro_transfers"

    class VerificationAddOns:
        """
        Constants representing verification add on types. Available statuses are:

        * braintree.UsBankAccountVerification.VerificationAddOns.CustomerVerification
        """

        CustomerVerification: Final = "customer_verification"

    us_bank_account: UsBankAccount | None
    def __init__(self, gateway, attributes) -> None: ...
    @staticmethod
    def confirm_micro_transfer_amounts(verification_id: str, amounts) -> SuccessfulResult | ErrorResult | None: ...
    @staticmethod
    def find(verification_id: str) -> UsBankAccountVerification: ...
    @staticmethod
    def search(*query) -> ResourceCollection: ...
    def __eq__(self, other: object) -> bool: ...
