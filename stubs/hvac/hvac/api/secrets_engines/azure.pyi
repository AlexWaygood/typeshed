"""Azure secret engine methods module."""

from hvac.api.vault_api_base import VaultApiBase

DEFAULT_MOUNT_POINT: str

class Azure(VaultApiBase):
    """Azure Secrets Engine (API).

    Reference: https://www.vaultproject.io/api/secret/azure/index.html
    """

    def configure(self, subscription_id, tenant_id, client_id=None, client_secret=None, environment=None, mount_point="azure"):
        """Configure the credentials required for the plugin to perform API calls to Azure.

        These credentials will be used to query roles and create/delete service principals. Environment variables will
        override any parameters set in the config.

        Supported methods:
            POST: /{mount_point}/config. Produces: 204 (empty body)


        :param subscription_id: The subscription id for the Azure Active Directory
        :type subscription_id: str | unicode
        :param tenant_id: The tenant id for the Azure Active Directory.
        :type tenant_id: str | unicode
        :param client_id: The OAuth2 client id to connect to Azure.
        :type client_id: str | unicode
        :param client_secret: The OAuth2 client secret to connect to Azure.
        :type client_secret: str | unicode
        :param environment: The Azure environment. If not specified, Vault will use Azure Public Cloud.
        :type environment: str | unicode
        :param mount_point: The OAuth2 client secret to connect to Azure.
        :type mount_point: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """

    def read_config(self, mount_point="azure"):
        """Read the stored configuration, omitting client_secret.

        Supported methods:
            GET: /{mount_point}/config. Produces: 200 application/json


        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The data key from the JSON response of the request.
        :rtype: dict
        """

    def delete_config(self, mount_point="azure"):
        """Delete the stored Azure configuration and credentials.

        Supported methods:
            DELETE: /auth/{mount_point}/config. Produces: 204 (empty body)


        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """

    def create_or_update_role(self, name, azure_roles, ttl=None, max_ttl=None, mount_point="azure"):
        """Create or update a Vault role.

        The provided Azure roles must exist for this call to succeed. See the Azure secrets roles docs for more
        information about roles.

        Supported methods:
            POST: /{mount_point}/roles/{name}. Produces: 204 (empty body)


        :param name: Name of the role.
        :type name: str | unicode
        :param azure_roles:  List of Azure roles to be assigned to the generated service principal.
        :type azure_roles: list(dict)
        :param ttl: Specifies the default TTL for service principals generated using this role. Accepts time suffixed
            strings ("1h") or an integer number of seconds. Defaults to the system/engine default TTL time.
        :type ttl: str | unicode
        :param max_ttl: Specifies the maximum TTL for service principals generated using this role. Accepts time
            suffixed strings ("1h") or an integer number of seconds. Defaults to the system/engine max TTL time.
        :type max_ttl: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """

    def list_roles(self, mount_point="azure"):
        """List all of the roles that are registered with the plugin.

        Supported methods:
            LIST: /{mount_point}/roles. Produces: 200 application/json


        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The data key from the JSON response of the request.
        :rtype: dict
        """

    def generate_credentials(self, name, mount_point="azure"):
        """Generate a new service principal based on the named role.

        Supported methods:
            GET: /{mount_point}/creds/{name}. Produces: 200 application/json


        :param name: Specifies the name of the role to create credentials against.
        :type name: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The data key from the JSON response of the request.
        :rtype: dict
        """
