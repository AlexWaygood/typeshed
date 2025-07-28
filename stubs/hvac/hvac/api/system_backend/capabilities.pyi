from hvac.api.system_backend.system_backend_mixin import SystemBackendMixin

class Capabilities(SystemBackendMixin):
    def get_capabilities(self, paths, token=None, accessor=None):
        """Get the capabilities associated with a token.

        Supported methods:
            POST: /sys/capabilities-self. Produces: 200 application/json
            POST: /sys/capabilities. Produces: 200 application/json
            POST: /sys/capabilities-accessor. Produces: 200 application/json

        :param paths: Paths on which capabilities are being queried.
        :type paths: List[str]
        :param token: Token for which capabilities are being queried.
        :type token: str
        :param accessor: Accessor of the token for which capabilities are being queried.
        :type accessor: str
        :return: The JSON response of the request.
        :rtype: dict
        """
