from _typeshed import Incomplete

from .base import AuthenticationBase

class BackChannelLogin(AuthenticationBase):
    """Back-Channel Login endpoint"""

    def back_channel_login(
        self,
        binding_message: str,
        login_hint: str,
        scope: str,
        authorization_details: str | list[dict[str, Incomplete]] | None = None,
        **kwargs,
    ):
        """Send a Back-Channel Login.

        Args:
             binding_message (str): Human-readable string displayed on both the device calling /bc-authorize and the user’s
             authentication device to ensure the user is approves the correct request.

             login_hint (str):  JSON string containing user details for authentication in the iss_sub format.Ensure
             serialization before passing.

             scope(str): "openid" is a required scope.Multiple scopes are separated
             with whitespace.

             authorization_details (str, list of dict, optional): JSON string or a list of dictionaries representing
             Rich Authorization Requests (RAR) details to include in the CIBA request.

             **kwargs: Other fields to send along with the request.

        Returns:
            auth_req_id, expires_in, interval
        """
