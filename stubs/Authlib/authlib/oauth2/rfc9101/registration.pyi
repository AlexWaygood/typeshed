from authlib.jose import BaseClaims

class ClientMetadataClaims(BaseClaims):
    """Additional client metadata can be used with :ref:`specs/rfc7591` and :ref:`specs/rfc7592` endpoints.

    This can be used with::

        server.register_endpoint(
            ClientRegistrationEndpoint(
                claims_classes=[
                    rfc7591.ClientMetadataClaims,
                    rfc9101.ClientMetadataClaims,
                ]
            )
        )

        server.register_endpoint(
            ClientRegistrationEndpoint(
                claims_classes=[
                    rfc7591.ClientMetadataClaims,
                    rfc9101.ClientMetadataClaims,
                ]
            )
        )

    """

    def validate(self) -> None: ...
    def validate_require_signed_request_object(self) -> None: ...
