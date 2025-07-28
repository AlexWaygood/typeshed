"""Active Directory methods module."""

from hvac.api.vault_api_base import VaultApiBase

DEFAULT_MOUNT_POINT: str

class ActiveDirectory(VaultApiBase):
    """Active Directory Secrets Engine (API).
    Reference: https://www.vaultproject.io/api/secret/ad/index.html
    """

    def configure(
        self,
        binddn=None,
        bindpass=None,
        url=None,
        userdn=None,
        upndomain=None,
        ttl=None,
        max_ttl=None,
        mount_point="ad",
        *args,
        **kwargs,
    ):
        """Configure shared information for the ad secrets engine.

        Supported methods:
            POST: /{mount_point}/config. Produces: 204 (empty body)

        :param binddn: Distinguished name of object to bind when performing user and group search.
        :type binddn: str | unicode
        :param bindpass: Password to use along with binddn when performing user search.
        :type bindpass: str | unicode
        :param url: Base DN under which to perform user search.
        :type url: str | unicode
        :param userdn: Base DN under which to perform user search.
        :type userdn: str | unicode
        :param upndomain: userPrincipalDomain used to construct the UPN string for the authenticating user.
        :type upndomain: str | unicode
        :param ttl: – The default password time-to-live in seconds. Once the ttl has passed, a password will be rotated the next time it's requested.
        :type ttl: int | str
        :param max_ttl: The maximum password time-to-live in seconds. No role will be allowed to set a custom ttl greater than the max_ttl
            integer number of seconds or Go duration format string.**
        :type max_ttl: int | str
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """

    def read_config(self, mount_point="ad"):
        """Read the configured shared information for the ad secrets engine.

        Credentials will be omitted from returned data.

        Supported methods:
            GET: /{mount_point}/config. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: dict
        """

    def create_or_update_role(self, name, service_account_name=None, ttl=None, mount_point="ad"):
        """This endpoint creates or updates the ad role definition.

        :param name: Specifies the name of an existing role against which to create this ad credential.
        :type name: str | unicode
        :param service_account_name: The name of a pre-existing service account in Active Directory that maps to this role.
            This value is required on create and optional on update.
        :type service_account_name: str | unicode
        :param ttl: Specifies the TTL for this role.
            This is provided as a string duration with a time suffix like "30s" or "1h" or as seconds.
            If not provided, the default Vault TTL is used.
        :type ttl: str | unicode
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ad).
        :type mount_point: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """

    def read_role(self, name, mount_point="ad"):
        """This endpoint queries for information about a ad role with the given name.
        If no role exists with that name, a 404 is returned.
        :param name: Specifies the name of the role to query.
        :type name: str | unicode
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ad).
        :type mount_point: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """

    def list_roles(self, mount_point="ad"):
        """This endpoint lists all existing roles in the secrets engine.
        :return: The response of the request.
        :rtype: requests.Response
        """

    def delete_role(self, name, mount_point="ad"):
        """This endpoint deletes a ad role with the given name.
        Even if the role does not exist, this endpoint will still return a successful response.
        :param name: Specifies the name of the role to delete.
        :type name: str | unicode
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ad).
        :type mount_point: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """

    def generate_credentials(self, name, mount_point="ad"):
        """This endpoint retrieves the previous and current LDAP password for
           the associated account (or rotate if required)

        :param name: Specifies the name of the role to request credentials from.
        :type name: str | unicode
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: ad).
        :type mount_point: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """
