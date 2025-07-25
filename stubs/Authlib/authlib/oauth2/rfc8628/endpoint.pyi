from _typeshed import Incomplete

class DeviceAuthorizationEndpoint:
    """This OAuth 2.0 [RFC6749] protocol extension enables OAuth clients to
    request user authorization from applications on devices that have
    limited input capabilities or lack a suitable browser.  Such devices
    include smart TVs, media consoles, picture frames, and printers,
    which lack an easy input method or a suitable browser required for
    traditional OAuth interactions. Here is the authorization flow::

        +----------+                                +----------------+
        |          |>---(A)-- Client Identifier --->|                |
        |          |                                |                |
        |          |<---(B)-- Device Code,      ---<|                |
        |          |          User Code,            |                |
        |  Device  |          & Verification URI    |                |
        |  Client  |                                |                |
        |          |  [polling]                     |                |
        |          |>---(E)-- Device Code       --->|                |
        |          |          & Client Identifier   |                |
        |          |                                |  Authorization |
        |          |<---(F)-- Access Token      ---<|     Server     |
        +----------+   (& Optional Refresh Token)   |                |
              v                                     |                |
              :                                     |                |
             (C) User Code & Verification URI       |                |
              :                                     |                |
              v                                     |                |
        +----------+                                |                |
        | End User |                                |                |
        |    at    |<---(D)-- End user reviews  --->|                |
        |  Browser |          authorization request |                |
        +----------+                                +----------------+

    This DeviceAuthorizationEndpoint is the implementation of step (A) and (B).

    (A) The client requests access from the authorization server and
        includes its client identifier in the request.

    (B) The authorization server issues a device code and an end-user
        code and provides the end-user verification URI.
    """

    ENDPOINT_NAME: str
    CLIENT_AUTH_METHODS: Incomplete
    USER_CODE_TYPE: str
    EXPIRES_IN: int
    INTERVAL: int
    server: Incomplete
    def __init__(self, server) -> None: ...
    def __call__(self, request): ...
    def create_endpoint_request(self, request): ...
    def authenticate_client(self, request):
        """client_id is REQUIRED **if the client is not** authenticating with the
        authorization server as described in Section 3.2.1. of [RFC6749].

        This means the endpoint support "none" authentication method. In this case,
        this endpoint's auth methods are:

        - client_secret_basic
        - client_secret_post
        - none

        Developers change the value of ``CLIENT_AUTH_METHODS`` in subclass. For
        instance::

            class MyDeviceAuthorizationEndpoint(DeviceAuthorizationEndpoint):
                # only support ``client_secret_basic`` auth method
                CLIENT_AUTH_METHODS = ["client_secret_basic"]
        """

    def create_endpoint_response(self, request): ...
    def generate_user_code(self):
        """A method to generate ``user_code`` value for device authorization
        endpoint. This method will generate a random string like MQNA-JPOZ.
        Developers can rewrite this  method to create their own ``user_code``.
        """

    def generate_device_code(self):
        """A method to generate ``device_code`` value for device authorization
        endpoint. This method will generate a random string of 42 characters.
        Developers can rewrite this method to create their own ``device_code``.
        """

    def get_verification_uri(self) -> None:
        """Define the ``verification_uri`` of device authorization endpoint.
        Developers MUST implement this method in subclass::

            def get_verification_uri(self):
                return "https://your-company.com/active"
        """

    def save_device_credential(self, client_id, scope, data) -> None:
        """Save device token into database for later use. Developers MUST
        implement this method in subclass::

            def save_device_credential(self, client_id, scope, data):
                item = DeviceCredential(client_id=client_id, scope=scope, **data)
                item.save()
        """

def create_string_user_code(): ...
def create_digital_user_code(): ...
