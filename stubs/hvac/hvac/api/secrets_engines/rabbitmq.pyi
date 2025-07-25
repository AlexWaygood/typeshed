"""RabbitMQ vault secrets backend module."""

from hvac.api.vault_api_base import VaultApiBase

DEFAULT_MOUNT_POINT: str

class RabbitMQ(VaultApiBase):
    """RabbitMQ Secrets Engine (API).
    Reference: https://www.vaultproject.io/api/secret/rabbitmq/index.html
    """

    def configure(
        self,
        connection_uri: str = "",
        username: str = "",
        password: str = "",
        verify_connection: bool = True,
        mount_point="rabbitmq",
    ):
        """Configure shared information for the rabbitmq secrets engine.

        Supported methods:
            POST: /{mount_point}/config/connection. Produces: 204 (empty body)

        :param connection_uri: Specifies the RabbitMQ connection URI.
        :type connection_uri: str | unicode
        :param username: Specifies the RabbitMQ management administrator username.
        :type username: str | unicode
        :password: Specifies the RabbitMQ management administrator password.
        :type password: str | unicode
        :verify_connection: Specifies whether to verify connection URI, username, and password.
        :type verify_connection: bool
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: rabbitmq).
        :type mount_point: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """

    def configure_lease(self, ttl, max_ttl, mount_point="rabbitmq"):
        """This endpoint configures the lease settings for generated credentials.

        :param ttl: Specifies the lease ttl provided in seconds.
        :type ttl: int
        :param max_ttl: Specifies the maximum ttl provided in seconds.
        :type max_ttl: int
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: rabbitmq).
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def create_role(self, name, tags: str = "", vhosts: str = "", vhost_topics: str = "", mount_point: str = "rabbitmq"):
        """This endpoint creates or updates the role definition.

        :param name:  Specifies the name of the role to create.
        :type name: str | unicode
        :param tags:  Specifies a comma-separated RabbitMQ management tags.
        :type tags: str | unicode
        :param vhosts:  pecifies a map of virtual hosts to permissions.
        :type vhosts: str | unicode
        :param vhost_topics: Specifies a map of virtual hosts and exchanges to topic permissions.
        :type vhost_topics: str | unicode
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: rabbitmq).
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def read_role(self, name, mount_point="rabbitmq"):
        """This endpoint queries the role definition.

        :param name:  Specifies the name of the role to read.
        :type name: str | unicode
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: rabbitmq).
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def delete_role(self, name, mount_point="rabbitmq"):
        """This endpoint deletes the role definition.
        Even if the role does not exist, this endpoint will still return a successful response.

        :param name: Specifies the name of the role to delete.
        :type name: str | unicode
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: rabbitmq).
        :type mount_point: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """

    def generate_credentials(self, name, mount_point="rabbitmq"):
        """This endpoint generates a new set of dynamic credentials based on the named role.

        :param name: Specifies the name of the role to create credentials against.
        :type name: str | unicode
        :param mount_point: Specifies the place where the secrets engine will be accessible (default: rabbitmq).
        :type mount_point: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """
