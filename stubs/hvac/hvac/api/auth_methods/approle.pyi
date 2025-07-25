"""APPROLE methods module."""

from hvac.api.vault_api_base import VaultApiBase

class AppRole(VaultApiBase):
    """USERPASS Auth Method (API).
    Reference: https://www.vaultproject.io/api-docs/auth/approle/index.html
    """

    def create_or_update_approle(
        self,
        role_name,
        bind_secret_id=None,
        secret_id_bound_cidrs=None,
        secret_id_num_uses=None,
        secret_id_ttl=None,
        enable_local_secret_ids=None,
        token_ttl=None,
        token_max_ttl=None,
        token_policies=None,
        token_bound_cidrs=None,
        token_explicit_max_ttl=None,
        token_no_default_policy=None,
        token_num_uses=None,
        token_period=None,
        token_type=None,
        mount_point="approle",
    ):
        """
        Create/update approle.

        Supported methods:
            POST: /auth/{mount_point}/role/{role_name}. Produces: 204 (empty body)

        :param role_name: The name for the approle.
        :type role_name: str | unicode
        :param bind_secret_id: Require secret_id to be presented when logging in using this approle.
        :type bind_secret_id: bool
        :param secret_id_bound_cidrs: Blocks of IP addresses which can perform login operations.
        :type secret_id_bound_cidrs: list
        :param secret_id_num_uses: Number of times any secret_id can be used to fetch a token.
            A value of zero allows unlimited uses.
        :type secret_id_num_uses: int
        :param secret_id_ttl: Duration after which a secret_id expires. This can be specified
            as an integer number of seconds or as a duration value like "5m".
        :type secret_id_ttl: str | unicode
        :param enable_local_secret_ids: Secret IDs generated using role will be cluster local.
        :type enable_local_secret_ids: bool
        :param token_ttl: Incremental lifetime for generated tokens. This can be specified
            as an integer number of seconds or as a duration value like "5m".
        :type token_ttl: str | unicode
        :param token_max_ttl: Maximum lifetime for generated tokens: This can be specified
            as an integer number of seconds or as a duration value like "5m".
        :type token_max_ttl: str | unicode
        :param token_policies: List of policies to encode onto generated tokens.
        :type token_policies: list
        :param token_bound_cidrs: Blocks of IP addresses which can authenticate successfully.
        :type token_bound_cidrs: list
        :param token_explicit_max_ttl: If set, will encode an explicit max TTL onto the token. This can be specified
            as an integer number of seconds or as a duration value like "5m".
        :type token_explicit_max_ttl: str | unicode
        :param token_no_default_policy: Do not add the default policy to generated tokens, use only tokens
            specified in token_policies.
        :type token_no_default_policy: bool
        :param token_num_uses: Maximum number of times a generated token may be used. A value of zero
            allows unlimited uses.
        :type token_num_uses: int
        :param token_period: The period, if any, to set on the token. This can be specified
            as an integer number of seconds or as a duration value like "5m".
        :type token_period: str | unicode
        :param token_type: The type of token that should be generated, can be "service", "batch", or "default".
        :type token_type: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        """

    def list_roles(self, mount_point="approle"):
        """
        List existing roles created in the auth method.

        Supported methods:
            LIST: /auth/{mount_point}/role. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the list_roles request.
        :rtype: dict
        """

    def read_role(self, role_name, mount_point="approle"):
        """
        Read role in the auth method.

        Supported methods:
            GET: /auth/{mount_point}/role/{role_name}. Produces: 200 application/json

        :param role_name: The name for the role.
        :type role_name: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the read_role request.
        :rtype: dict
        """

    def delete_role(self, role_name, mount_point="approle"):
        """
        Delete role in the auth method.

        Supported methods:
            DELETE: /auth/{mount_point}/role/{role_name}. Produces: 204 (empty body)

        :param role_name: The name for the role.
        :type role_name: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        """

    def read_role_id(self, role_name, mount_point="approle"):
        """
        Reads the Role ID of a role in the auth method.

        Supported methods:
            GET: /auth/{mount_point}/role/{role_name}/role-id. Produces: 200 application/json

        :param role_name: The name for the role.
        :type role_name: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the read_role_id request.
        :rtype: dict
        """

    def update_role_id(self, role_name, role_id, mount_point="approle"):
        """
        Updates the Role ID of a role in the auth method.

        Supported methods:
            POST: /auth/{mount_point}/role/{role_name}/role-id. Produces: 200 application/json

        :param role_name: The name for the role.
        :type role_name: str | unicode
        :param role_id: New value for the Role ID.
        :type role_id: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the read_role_id request.
        :rtype: dict
        """

    def generate_secret_id(
        self, role_name, metadata=None, cidr_list=None, token_bound_cidrs=None, mount_point="approle", wrap_ttl=None
    ):
        """
        Generates and issues a new Secret ID on a role in the auth method.

        Supported methods:
            POST: /auth/{mount_point}/role/{role_name}/secret-id. Produces: 200 application/json

        :param role_name: The name for the role.
        :type role_name: str | unicode
        :param metadata: Metadata to be tied to the Secret ID.
        :type metadata: dict
        :param cidr_list: Blocks of IP addresses which can perform login operations.
        :type cidr_list: list
        :param token_bound_cidrs: Blocks of IP addresses which can authenticate successfully.
        :type token_bound_cidrs: list
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :param wrap_ttl: Returns the request as a response-wrapping token.
            Can be either an integer number of seconds or a string duration of seconds (`15s`), minutes (`20m`), or hours (`25h`).
        :type wrap_ttl: int | str
        :return: The JSON response of the read_role_id request.
        :rtype: dict
        """

    def create_custom_secret_id(
        self, role_name, secret_id, metadata=None, cidr_list=None, token_bound_cidrs=None, mount_point="approle", wrap_ttl=None
    ):
        """
        Generates and issues a new Secret ID on a role in the auth method.

        Supported methods:
            POST: /auth/{mount_point}/role/{role_name}/custom-secret-id. Produces: 200 application/json

        :param role_name: The name for the role.
        :type role_name: str | unicode
        :param secret_id: The Secret ID to read.
        :type secret_id: str | unicode
        :param metadata: Metadata to be tied to the Secret ID.
        :type metadata: dict
        :param cidr_list: Blocks of IP addresses which can perform login operations.
        :type cidr_list: list
        :param token_bound_cidrs: Blocks of IP addresses which can authenticate successfully.
        :type token_bound_cidrs: list
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :param wrap_ttl: Returns the request as a response-wrapping token.
            Can be either an integer number of seconds or a string duration of seconds (`15s`), minutes (`20m`), or hours (`25h`).
        :type wrap_ttl: int | str
        :return: The JSON response of the read_role_id request.
        :rtype: dict
        """

    def read_secret_id(self, role_name, secret_id, mount_point="approle"):
        """
        Read the properties of a Secret ID for a role in the auth method.

        Supported methods:
            POST: /auth/{mount_point}/role/{role_name}/secret-id/lookup. Produces: 200 application/json

        :param role_name: The name for the role
        :type role_name: str | unicode
        :param secret_id: The Secret ID to read.
        :type secret_id: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the read_role_id request.
        :rtype: dict
        """

    def destroy_secret_id(self, role_name, secret_id, mount_point="approle"):
        """
        Destroys a Secret ID for a role in the auth method.

        Supported methods:
            POST: /auth/{mount_point}/role/{role_name}/secret-id/destroy. Produces 204 (empty body)

        :param role_name: The name for the role
        :type role_name: str | unicode
        :param secret_id: The Secret ID to read.
        :type secret_id: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        """

    def list_secret_id_accessors(self, role_name, mount_point="approle"):
        """
        Lists accessors of all issued Secret IDs for a role in the auth method.

        Supported methods:
            LIST: /auth/{mount_point}/role/{role_name}/secret-id. Produces: 200 application/json

        :param role_name: The name for the role
        :type role_name: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the read_role_id request.
        :rtype: dict
        """

    def read_secret_id_accessor(self, role_name, secret_id_accessor, mount_point="approle"):
        """
        Read the properties of a Secret ID for a role in the auth method.

        Supported methods:
            POST: /auth/{mount_point}/role/{role_name}/secret-id-accessor/lookup. Produces: 200 application/json

        :param role_name: The name for the role
        :type role_name: str | unicode
        :param secret_id_accessor: The accessor for the Secret ID to read.
        :type secret_id_accessor: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the read_role_id request.
        :rtype: dict
        """

    def destroy_secret_id_accessor(self, role_name, secret_id_accessor, mount_point="approle"):
        """
        Destroys a Secret ID for a role in the auth method.

        Supported methods:
            POST: /auth/{mount_point}/role/{role_name}/secret-id-accessor/destroy. Produces: 204 (empty body)

        :param role_name: The name for the role
        :type role_name: str | unicode
        :param secret_id_accessor: The accessor for the Secret ID to read.
        :type secret_id_accessor: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        """

    def login(self, role_id, secret_id=None, use_token: bool = True, mount_point="approle"):
        """
        Login with APPROLE credentials.

        Supported methods:
            POST: /auth/{mount_point}/login. Produces: 200 application/json

        :param role_id: Role ID of the role.
        :type role_id: str | unicode
        :param secret_id: Secret ID of the role.
        :type secret_id: str | unicode
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the the :py:meth:`hvac.adapters.Adapter` instance under the _adapter Client attribute.
        :type use_token: bool
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the read_role_id request.
        :rtype: dict
        """
