"""Github methods module."""

from hvac.api.vault_api_base import VaultApiBase

DEFAULT_MOUNT_POINT: str

class Github(VaultApiBase):
    """GitHub Auth Method (API).

    Reference: https://www.vaultproject.io/api/auth/github/index.html
    """

    def configure(self, organization, base_url=None, ttl=None, max_ttl=None, mount_point="github"):
        """Configure the connection parameters for GitHub.

        This path honors the distinction between the create and update capabilities inside ACL policies.

        Supported methods:
            POST: /auth/{mount_point}/config. Produces: 204 (empty body)


        :param organization: The organization users must be part of.
        :type organization: str | unicode
        :param base_url: The API endpoint to use. Useful if you are running GitHub Enterprise or an API-compatible
            authentication server.
        :type base_url: str | unicode
        :param ttl: Duration after which authentication will be expired.
        :type ttl: str | unicode
        :param max_ttl: Maximum duration after which authentication will
            be expired.
        :type max_ttl: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The response of the configure_method request.
        :rtype: requests.Response
        """

    def read_configuration(self, mount_point="github"):
        """Read the GitHub configuration.

        Supported methods:
            GET: /auth/{mount_point}/config. Produces: 200 application/json


        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the read_configuration request.
        :rtype: dict
        """

    def map_team(self, team_name, policies=None, mount_point="github"):
        """Map a list of policies to a team that exists in the configured GitHub organization.

        Supported methods:
            POST: /auth/{mount_point}/map/teams/{team_name}. Produces: 204 (empty body)


        :param team_name: GitHub team name in "slugified" format
        :type team_name: str | unicode
        :param policies: Comma separated list of policies to assign
        :type policies: List[str]
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The response of the map_github_teams request.
        :rtype: requests.Response
        """

    def read_team_mapping(self, team_name, mount_point="github"):
        """Read the GitHub team policy mapping.

        Supported methods:
            GET: /auth/{mount_point}/map/teams/{team_name}. Produces: 200 application/json


        :param team_name: GitHub team name
        :type team_name: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the read_team_mapping request.
        :rtype: dict
        """

    def map_user(self, user_name, policies=None, mount_point="github"):
        """Map a list of policies to a specific GitHub user exists in the configured organization.

        Supported methods:
            POST: /auth/{mount_point}/map/users/{user_name}. Produces: 204 (empty body)


        :param user_name: GitHub user name
        :type user_name: str | unicode
        :param policies: Comma separated list of policies to assign
        :type policies: List[str]
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The response of the map_github_users request.
        :rtype: requests.Response
        """

    def read_user_mapping(self, user_name, mount_point="github"):
        """Read the GitHub user policy mapping.

        Supported methods:
            GET: /auth/{mount_point}/map/users/{user_name}. Produces: 200 application/json


        :param user_name: GitHub user name
        :type user_name: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the read_user_mapping request.
        :rtype: dict
        """

    def login(self, token, use_token: bool = True, mount_point="github"):
        """Login using GitHub access token.

        Supported methods:
            POST: /auth/{mount_point}/login. Produces: 200 application/json


        :param token: GitHub personal API token.
        :type token: str | unicode
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the the :py:meth:`hvac.adapters.Adapter` instance under the _adapter Client attribute.
        :type use_token: bool
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the login request.
        :rtype: dict
        """
