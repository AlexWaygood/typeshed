from _typeshed import Incomplete

from ..rest import RestClientOptions
from ..types import TimeoutType

class Jobs:
    """Auth0 jobs endpoints

    Args:
        domain (str): Your Auth0 domain, e.g: 'username.auth0.com'

        token (str): Management API v2 Token

        telemetry (bool, optional): Enable or disable Telemetry
            (defaults to True)

        timeout (float or tuple, optional): Change the requests
            connect and read timeout. Pass a tuple to specify
            both values separately or a float to set both to it.
            (defaults to 5.0 for both)

        protocol (str, optional): Protocol to use when making requests.
            (defaults to "https")

        rest_options (RestClientOptions): Pass an instance of
            RestClientOptions to configure additional RestClient
            options, such as rate-limit retries.
            (defaults to None)
    """

    domain: Incomplete
    protocol: Incomplete
    client: Incomplete
    def __init__(
        self,
        domain: str,
        token: str,
        telemetry: bool = True,
        timeout: TimeoutType = 5.0,
        protocol: str = "https",
        rest_options: RestClientOptions | None = None,
    ) -> None: ...
    def get(self, id: str) -> dict[str, Incomplete]:
        """Retrieves a job. Useful to check its status.

        Args:
            id (str): The id of the job.

        See: https://auth0.com/docs/api/management/v2#!/Jobs/get_jobs_by_id
        """

    async def get_async(self, id: str) -> dict[str, Incomplete]: ...
    def get_failed_job(self, id: str) -> dict[str, Incomplete]:
        """Get failed job error details.

        Args:
            id (str): The id of the job.

        See: https://auth0.com/docs/api/management/v2#!/Jobs/get_errors
        """

    async def get_failed_job_async(self, id: str) -> dict[str, Incomplete]: ...
    def export_users(self, body: dict[str, Incomplete]):
        """Export all users to a file using a long running job.

        Check job status with get(). URL pointing to the export file will be
        included in the status once the job is complete.

        Args:
            body (dict): The details of the export users request.

        See: https://auth0.com/docs/api/management/v2#!/Jobs/post_users_exports
        """

    async def export_users_async(self, body: dict[str, Incomplete]): ...
    def import_users(
        self,
        connection_id: str,
        file_obj,
        upsert: bool = False,
        send_completion_email: bool = True,
        external_id: str | None = None,
    ) -> dict[str, Incomplete]:
        """Imports users to a connection from a file.

        Args:
            connection_id (str): The connection id of the connection to which
                users will be inserted.

            file_obj (file): A file-like object to upload. The format for
                this file is explained in: https://auth0.com/docs/bulk-import.

            upsert (bool, optional): When set to False, pre-existing users that match on email address, user ID, or username
                will fail. When set to True, pre-existing users that match on any of these fields will be updated, but
                only with upsertable attributes. Defaults to False.
                For a list of user profile fields that can be upserted during import, see the following article
                https://auth0.com/docs/users/references/user-profile-structure#user-profile-attributes.

            send_completion_email (bool, optional): When set to True, an email will be sent to notify the completion of this job.
                When set to False, no email will be sent. Defaults to True.

            external_id (str, optional):  Customer-defined ID.

        See: https://auth0.com/docs/api/management/v2#!/Jobs/post_users_imports
        """

    async def import_users_async(
        self,
        connection_id: str,
        file_obj,
        upsert: bool = False,
        send_completion_email: bool = True,
        external_id: str | None = None,
    ) -> dict[str, Incomplete]: ...
    def send_verification_email(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]:
        """Send verification email.

        Send an email to the specified user that asks them to click a link to
        verify their email address.

        Args:
            body (dict): Details of verification email request.

        See: https://auth0.com/docs/api/v2#!/Jobs/post_verification_email
        """

    async def send_verification_email_async(self, body: dict[str, Incomplete]) -> dict[str, Incomplete]: ...
