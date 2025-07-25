from _typeshed import Incomplete

class AuthorizationServerMetadata(dict[str, object]):
    REGISTRY_KEYS: Incomplete
    def validate_require_signed_request_object(self) -> None:
        """Indicates where authorization request needs to be protected as Request Object and provided through either request or request_uri parameter."""
