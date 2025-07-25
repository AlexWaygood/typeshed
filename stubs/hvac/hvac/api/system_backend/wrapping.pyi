from _typeshed import Incomplete

from hvac.api.system_backend.system_backend_mixin import SystemBackendMixin

class Wrapping(SystemBackendMixin):
    def unwrap(self, token=None):
        """Return the original response inside the given wrapping token.

        Unlike simply reading cubbyhole/response (which is deprecated), this endpoint provides additional validation
        checks on the token, returns the original value on the wire rather than a JSON string representation of it, and
        ensures that the response is properly audit-logged.

        Supported methods:
            POST: /sys/wrapping/unwrap. Produces: 200 application/json

        :param token: Specifies the wrapping token ID. This is required if the client token is not the wrapping token.
            Do not use the wrapping token in both locations.
        :type token: str | unicode
        :return: The JSON response of the request.
        :rtype: dict
        """

    def wrap(self, payload: dict[Incomplete, Incomplete] | None = None, ttl: int = 60):
        """Wraps a serializable dictionary inside a wrapping token.

        Supported methods:
            POST: /sys/wrapping/wrap. Produces: 200 application/json

        :param payload: Specifies the data that should be wrapped inside the token.
        :type payload: dict
        :param ttl: The TTL of the returned wrapping token.
        :type ttl: int
        :return: The JSON response of the request.
        :rtype: dict
        """
