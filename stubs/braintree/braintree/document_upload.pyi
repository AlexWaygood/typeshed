from _typeshed import Incomplete
from typing import Final

from braintree.error_result import ErrorResult
from braintree.resource import Resource
from braintree.successful_result import SuccessfulResult

class DocumentUpload(Resource):
    """
    A class representing a DocumentUpload.

    An example of creating a document upload with all available fields:

        result = braintree.DocumentUpload.create(
            {
                "kind": braintree.DocumentUpload.Kind.EvidenceDocument,
                "file": open("path/to/file", "rb"),
            }
        )

    For more information on DocumentUploads, see https://developer.paypal.com/braintree/docs/reference/request/document-upload/create

    """

    class Kind:
        EvidenceDocument: Final = "evidence_document"

    @staticmethod
    def create(params: dict[str, Incomplete] | None = None) -> SuccessfulResult | ErrorResult:
        """
        Create a DocumentUpload

        File and Kind are required:

            result = braintree.DocumentUpload.create(
                {
                    "kind": braintree.DocumentUpload.Kind.EvidenceDocument,
                    "file": open("path/to/file", "rb"),
                }
            )

        """

    @staticmethod
    def create_signature() -> list[str]: ...
    def __init__(self, gateway, attributes) -> None: ...
