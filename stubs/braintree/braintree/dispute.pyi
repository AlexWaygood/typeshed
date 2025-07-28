from _typeshed import Incomplete
from decimal import Decimal
from typing import Final

from braintree.attribute_getter import AttributeGetter
from braintree.dispute_details import DisputeEvidence, DisputePayPalMessage, DisputeStatusHistory
from braintree.error_result import ErrorResult
from braintree.successful_result import SuccessfulResult
from braintree.transaction_details import TransactionDetails

class Dispute(AttributeGetter):
    class Status:
        """
        Constants representing dispute statuses. Available types are:

        * braintree.Dispute.Status.Accepted
        * braintree.Dispute.Status.AutoAccepted
        * braintree.Dispute.Status.Disputed
        * braintree.Dispute.Status.Expired
        * braintree.Dispute.Status.Lost
        * braintree.Dispute.Status.Open
        * braintree.Dispute.Status.UnderReview
        * braintree.Dispute.Status.Won
        """

        Accepted: Final = "accepted"
        AutoAccepted: Final = "auto_accepted"
        Disputed: Final = "disputed"
        Expired: Final = "expired"
        Lost: Final = "lost"
        Open: Final = "open"
        UnderReview: Final = "under_review"
        Won: Final = "won"

    class Reason:
        """
        Constants representing dispute reasons. Available types are:

        * braintree.Dispute.Reason.CancelledRecurringTransaction
        * braintree.Dispute.Reason.CreditNotProcessed
        * braintree.Dispute.Reason.Duplicate
        * braintree.Dispute.Reason.Fraud
        * braintree.Dispute.Reason.General
        * braintree.Dispute.Reason.InvalidAccount
        * braintree.Dispute.Reason.NotRecognized
        * braintree.Dispute.Reason.ProductNotReceived
        * braintree.Dispute.Reason.ProductUnsatisfactory
        * braintree.Dispute.Reason.Retrieval
        * braintree.Dispute.Reason.TransactionAmountDiffers
        """

        CancelledRecurringTransaction: Final = "cancelled_recurring_transaction"
        CreditNotProcessed: Final = "credit_not_processed"
        Duplicate: Final = "duplicate"
        Fraud: Final = "fraud"
        General: Final = "general"
        InvalidAccount: Final = "invalid_account"
        NotRecognized: Final = "not_recognized"
        ProductNotReceived: Final = "product_not_received"
        ProductUnsatisfactory: Final = "product_unsatisfactory"
        Retrieval: Final = "retrieval"
        TransactionAmountDiffers: Final = "transaction_amount_differs"

    class Kind:
        """
        Constants representing dispute kinds. Available types are:

        * braintree.Dispute.Kind.Chargeback
        * braintree.Dispute.Kind.PreArbitration
        * braintree.Dispute.Kind.Retrieval
        """

        Chargeback: Final = "chargeback"
        PreArbitration: Final = "pre_arbitration"
        Retrieval: Final = "retrieval"

    class ChargebackProtectionLevel:
        """
        Constants representing dispute ChargebackProtectionLevel. Available types are:

        * braintree.Dispute.ChargebackProtectionLevel.EFFORTLESS
        * braintree.Dispute.ChargebackProtectionLevel.STANDARD
        * braintree.Dispute.ChargebackProtectionLevel.NOT_PROTECTED
        """

        Effortless: Final = "effortless"
        Standard: Final = "standard"
        NotProtected: Final = "not_protected"

    class PreDisputeProgram:
        """
        Constants representing dispute pre-dispute programs. Available types are:

        * braintree.Dispute.PreDisputeProgram.NONE
        * braintree.Dispute.PreDisputeProgram.VisaRdr
        """

        NONE: Final = "none"
        VisaRdr: Final = "visa_rdr"

    class ProtectionLevel:
        """
        Constants representing dispute ProtectionLevel. Available types are:

        * braintree.Dispute.ProtectionLevel.EffortlessCBP
        * braintree.Dispute.ProtectionLevel.StandardCBP
        * braintree.Dispute.ProtectionLevel.NoProtection
        """

        EffortlessCBP: Final = "Effortless Chargeback Protection tool"
        StandardCBP: Final = "Chargeback Protection tool"
        NoProtection: Final = "No Protection"

    @staticmethod
    def accept(id: str) -> SuccessfulResult | ErrorResult:
        """
        Accept a dispute, given a dispute_id.
        This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>` if the provided dispute_id
        is not found. ::

            result = braintree.Dispute.accept("my_dispute_id")
        """

    @staticmethod
    def add_file_evidence(dispute_id: str, document_upload_id) -> SuccessfulResult | ErrorResult | None:
        """
        Adds file evidence to a dispute, given a dispute_id and a document_upload_id.

        This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>` if the provided dispute_id
        is not found. ::

            document = braintree.DocumentUpload.create({
                "kind": braintree.DocumentUpload.Kind.EvidenceDocument,
                "file": open("/path/to/evidence.pdf", "rb")
            })

            result = braintree.Dispute.add_file_evidence("my_dispute_id", document.id)
        """

    @staticmethod
    def add_text_evidence(id: str, content_or_request) -> SuccessfulResult | ErrorResult | None:
        """
        Adds text evidence to a dispute, given a dispute_id.

        This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>` if the provided dispute_id
        is not found. ::

            result = braintree.Dispute.add_text_evidence("my_dispute_id", "my_evidence")

            or

            result = braintree.Dispute.add_text_evidence("my_dispute_id", { "content": "UPS", "tag": "CARRIER_NAME", "sequence_number": "1" })
        """

    @staticmethod
    def finalize(id: str) -> SuccessfulResult | ErrorResult:
        """
        Finalize a dispute, given a dispute_id.
        This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>` if the provided dispute_id
        is not found. ::

            result = braintree.Dispute.finalize("my_dispute_id")
        """

    @staticmethod
    def find(id: str) -> Dispute:
        """
        Find an dispute, given a dispute_id.  This does not return a result
        object.  This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>` if the provided dispute_id
        is not found. ::

            dispute = braintree.Dispute.find("my_dispute_id")
        """

    @staticmethod
    def remove_evidence(id: str, evidence_id: str) -> SuccessfulResult | ErrorResult:
        """
        Remove evidence on a dispute.
        This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>` if the provided dispute_id or evidence_id
        is not found. ::

            result = braintree.Dispute.remove_evidence("my_dispute_id", "my_evidence_id")
        """

    @staticmethod
    def search(*query) -> SuccessfulResult:
        """
        Searches for disputes, given a DisputeSearch query.

            collection = braintree.Dispute.search([
                braintree.DisputeSearch.id == "the_dispute_id"
            ])

            for dispute in collection.items:
                print dispute.id
        """
    amount: Decimal | None
    amount_disputed: Decimal | None
    amount_won: Decimal | None
    protection_level: Incomplete
    transaction_details: TransactionDetails
    transaction = transaction_details
    evidence: list[DisputeEvidence] | None
    paypal_messages: list[DisputePayPalMessage] | None
    status_history: list[DisputeStatusHistory] | None
    processor_comments: Incomplete
    forwarded_comments: processor_comments
    def __init__(self, attributes) -> None: ...
