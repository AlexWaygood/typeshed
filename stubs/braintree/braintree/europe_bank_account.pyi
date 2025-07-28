from typing import Final

from braintree.resource import Resource

class EuropeBankAccount(Resource):
    class MandateType:
        """
        Constants representing the type of the mandate.  Available type:
        * Braintree.EuropeBankAccount.MandateType.Business
        * Braintree.EuropeBankAccount.MandateType.Consumer
        """

        Business: Final = "business"
        Consumer: Final = "consumer"

    @staticmethod
    def signature() -> list[str]: ...
