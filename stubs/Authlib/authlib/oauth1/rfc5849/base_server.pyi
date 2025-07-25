from _typeshed import Incomplete

class BaseServer:
    SIGNATURE_METHODS: Incomplete
    SUPPORTED_SIGNATURE_METHODS: Incomplete
    EXPIRY_TIME: int
    @classmethod
    def register_signature_method(cls, name, verify) -> None:
        """Extend signature method verification.

        :param name: A string to represent signature method.
        :param verify: A function to verify signature.

        The ``verify`` method accept ``OAuth1Request`` as parameter::

            def verify_custom_method(request):
                # verify this request, return True or False
                return True


            Server.register_signature_method("custom-name", verify_custom_method)
        """

    def validate_timestamp_and_nonce(self, request) -> None:
        """Validate ``oauth_timestamp`` and ``oauth_nonce`` in HTTP request.

        :param request: OAuth1Request instance
        """

    def validate_oauth_signature(self, request) -> None:
        """Validate ``oauth_signature`` from HTTP request.

        :param request: OAuth1Request instance
        """

    def get_client_by_id(self, client_id) -> None:
        """Get client instance with the given ``client_id``.

        :param client_id: A string of client_id
        :return: Client instance
        """

    def exists_nonce(self, nonce, request) -> None:
        """The nonce value MUST be unique across all requests with the same
        timestamp, client credentials, and token combinations.

        :param nonce: A string value of ``oauth_nonce``
        :param request: OAuth1Request instance
        :return: Boolean
        """
