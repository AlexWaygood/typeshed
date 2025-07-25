from hvac.api.system_backend.system_backend_mixin import SystemBackendMixin

class Policies(SystemBackendMixin):
    def list_acl_policies(self):
        """List all configured acl policies.

        Supported methods:
            GET: /sys/policies/acl. Produces: 200 application/json

        :return: The JSON response of the request.
        :rtype: dict
        """

    def read_acl_policy(self, name):
        """Retrieve the policy body for the named acl policy.

        Supported methods:
            GET: /sys/policies/acl/{name}. Produces: 200 application/json

        :param name: The name of the acl policy to retrieve.
        :type name: str | unicode
        :return: The response of the request
        :rtype: dict
        """

    def create_or_update_acl_policy(self, name, policy, pretty_print: bool = True):
        """Add a new or update an existing acl policy.

        Once a policy is updated, it takes effect immediately to all associated users.

        Supported methods:
            PUT: /sys/policies/acl/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the policy to create.
        :type name: str | unicode
        :param policy: Specifies the policy to create or update.
        :type policy: str | unicode | dict
        :param pretty_print: If True, and provided a dict for the policy argument, send the policy JSON to Vault with
            "pretty" formatting.
        :type pretty_print: bool
        :return: The response of the request.
        :rtype: requests.Response
        """

    def delete_acl_policy(self, name):
        """Delete the acl policy with the given name.

        This will immediately affect all users associated with this policy.

        Supported methods:
            DELETE: /sys/policies/acl/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the policy to delete.
        :type name: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """

    def list_rgp_policies(self):
        """List all configured rgp policies.

        Supported methods:
            GET: /sys/policies/rgp. Produces: 200 application/json

        :return: The JSON response of the request.
        :rtype: dict
        """

    def read_rgp_policy(self, name):
        """Retrieve the policy body for the named rgp policy.

        Supported methods:
            GET: /sys/policies/rgp/{name}. Produces: 200 application/json

        :param name: The name of the rgp policy to retrieve.
        :type name: str | unicode
        :return: The response of the request
        :rtype: dict
        """

    def create_or_update_rgp_policy(self, name, policy, enforcement_level):
        """Add a new or update an existing rgp policy.

        Once a policy is updated, it takes effect immediately to all associated users.

        Supported methods:
            PUT: /sys/policies/rgp/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the policy to create.
        :type name: str | unicode
        :param policy: Specifies the policy to create or update.
        :type policy: str | unicode
        :param enforcement_level: Specifies the enforcement level to use. This must be one of advisory, soft-mandatory, or hard-mandatory
        :type enforcement_level: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """

    def delete_rgp_policy(self, name):
        """Delete the rgp policy with the given name.

        This will immediately affect all users associated with this policy.

        Supported methods:
            DELETE: /sys/policies/rgp/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the policy to delete.
        :type name: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """

    def list_egp_policies(self):
        """List all configured egp policies.

        Supported methods:
            GET: /sys/policies/egp. Produces: 200 application/json

        :return: The JSON response of the request.
        :rtype: dict
        """

    def read_egp_policy(self, name):
        """Retrieve the policy body for the named egp policy.

        Supported methods:
            GET: /sys/policies/egp/{name}. Produces: 200 application/json

        :param name: The name of the egp policy to retrieve.
        :type name: str | unicode
        :return: The response of the request
        :rtype: dict
        """

    def create_or_update_egp_policy(self, name, policy, enforcement_level, paths):
        """Add a new or update an existing egp policy.

        Once a policy is updated, it takes effect immediately to all associated users.

        Supported methods:
            PUT: /sys/policies/egp/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the policy to create.
        :type name: str | unicode
        :param policy: Specifies the policy to create or update.
        :type policy: str | unicode
        :param enforcement_level: Specifies the enforcement level to use. This must be one of advisory, soft-mandatory, or hard-mandatory
        :type enforcement_level: str | unicode
        :param paths: Specifies the paths on which this EGP should be applied.
        :type paths: list
        :return: The response of the request.
        :rtype: requests.Response
        """

    def delete_egp_policy(self, name):
        """Delete the egp policy with the given name.

        This will immediately affect all users associated with this policy.

        Supported methods:
            DELETE: /sys/policies/egp/{name}. Produces: 204 (empty body)

        :param name: Specifies the name of the policy to delete.
        :type name: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """
