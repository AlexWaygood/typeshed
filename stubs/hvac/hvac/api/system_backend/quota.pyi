from hvac.api.system_backend.system_backend_mixin import SystemBackendMixin

class Quota(SystemBackendMixin):
    def read_quota(self, name):
        """Read quota. Only works when calling on the root namespace.

        Supported methods:
            GET: /sys/quotas/rate-limit/:name. Produces: 200 application/json

        :param name: the name of the quota to look up.
        :type name: str | unicode
        :return: JSON response from API request.
        :rtype: requests.Response
        """

    def list_quotas(self):
        """Retrieve a list of quotas by name. Only works when calling on the root namespace.

        Supported methods:
            LIST: /sys/quotas/rate-limit. Produces: 200 application/json

        :return: JSON response from API request.
        :rtype: requests.Response
        """

    def create_or_update_quota(
        self, name, rate, path=None, interval=None, block_interval=None, role=None, rate_limit_type=None, inheritable=None
    ):
        """Create quota if it doesn't exist or update if already created. Only works when calling on the root namespace.

        Supported methods:
            POST: /sys/quotas/rate-limit. Produces: 204 (empty body)

        :param name: The name of the quota to create or update.
        :type name: str | unicode
        :param path: Path of the mount or namespace to apply the quota.
        :type path: str | unicode
        :param rate: The maximum number of requests in a given interval to be allowed. Must be positive.
        :type rate: float
        :param interval: The duration to enforce rate limit. Default is "1s".
        :type interval: str | unicode
        :param block_interval: If rate limit is reached, how long before client can send requests again.
        :type block_interval: str | unicode
        :param role: If quota is set on an auth mount path, restrict login requests that are made with a specified role.
        :type role: str | unicode
        :param rate_limit_type: Type of rate limit quota. Can be lease-count or rate-limit.
        :type rate_limit_type: str | unicode
        :param inheritable: If set to true on a path that is a namespace, quota will be applied to all child namespaces
        :type inheritable: bool
        :return: API status code from request.
        :rtype: requests.Response
        """

    def delete_quota(self, name):
        """Delete a given quota. Only works when calling on the root namespace.

        Supported methods:
            DELETE: /sys/quotas/rate-limit. Produces: 204 (empty body)

        :param name: Name of the quota to delete
        :type name: str | unicode
        :return: API status code from request.
        :rtype: requests.Response
        """
