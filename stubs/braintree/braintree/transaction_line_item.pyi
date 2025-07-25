from typing import Final

from braintree.attribute_getter import AttributeGetter

class TransactionLineItem(AttributeGetter):
    class Kind:
        """
        Constants representing transaction line item kinds. Available kinds are:

        * braintree.TransactionLineItem.Kind.Credit
        * braintree.TransactionLineItem.Kind.Debit
        """

        Credit: Final = "credit"
        Debit: Final = "debit"

    def __init__(self, attributes) -> None: ...
    @staticmethod
    def find_all(transaction_id):
        """
        Find all line items on a transaction, given a transaction_id. This returns an array of TransactionLineItems.
        This will raise a :class:`NotFoundError <braintree.exceptions.not_found_error.NotFoundError>` if the provided
        transaction_id is not found. ::

            transaction_line_items = braintree.TransactionLineItem.find_all("my_transaction_id")
        """
