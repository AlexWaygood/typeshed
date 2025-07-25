from .base import AuthenticationBase

class GetToken(AuthenticationBase):
    """/oauth/token related endpoints

    Args:
        domain (str): Your auth0 domain (e.g: username.auth0.com)
    """

    def authorization_code(self, code: str, redirect_uri: str | None, grant_type: str = "authorization_code"):
        """Authorization code grant

        This is the OAuth 2.0 grant that regular web apps utilize in order
        to access an API. Use this endpoint to exchange an Authorization Code
        for a Token.

        Args:
            code (str): The Authorization Code received from the /authorize Calls

            redirect_uri (str, optional): This is required only if it was set at
            the GET /authorize endpoint. The values must match

            grant_type (str): Denotes the flow you're using. For authorization code
            use authorization_code

        Returns:
            access_token, id_token
        """

    def authorization_code_pkce(
        self, code_verifier: str, code: str, redirect_uri: str | None, grant_type: str = "authorization_code"
    ):
        """Authorization code pkce grant

        This is the OAuth 2.0 grant that mobile apps utilize in order to access an API.
        Use this endpoint to exchange an Authorization Code for a Token.

        Args:
            code_verifier (str): Cryptographically random key that was used to generate
            the code_challenge passed to /authorize.

            code (str): The Authorization Code received from the /authorize Calls

            redirect_uri (str, optional): This is required only if it was set at
            the GET /authorize endpoint. The values must match

            grant_type (str): Denotes the flow you're using. For authorization code pkce
            use authorization_code

        Returns:
            access_token, id_token
        """

    def client_credentials(self, audience: str, grant_type: str = "client_credentials", organization: str | None = None):
        """Client credentials grant

        This is the OAuth 2.0 grant that server processes utilize in
        order to access an API. Use this endpoint to directly request
        an access_token by using the Application Credentials (a Client Id and
        a Client Secret).

        Args:
            audience (str): The unique identifier of the target API you want to access.

            grant_type (str, optional): Denotes the flow you're using. For client credentials use "client_credentials"

            organization (str, optional): Optional Organization name or ID. When included, the access token returned
            will include the org_id and org_name claims

        Returns:
            access_token
        """

    def login(
        self,
        username: str,
        password: str,
        scope: str | None = None,
        realm: str | None = None,
        audience: str | None = None,
        grant_type: str = "http://auth0.com/oauth/grant-type/password-realm",
        forwarded_for: str | None = None,
    ):
        """Calls /oauth/token endpoint with password-realm grant type


        This is the OAuth 2.0 grant that highly trusted apps utilize in order
        to access an API. In this flow the end-user is asked to fill in credentials
        (username/password) typically using an interactive form in the user-agent
        (browser). This information is later on sent to the client and Auth0.
        It is therefore imperative that the client is absolutely trusted with
        this information.

        Args:
            username (str): Resource owner's identifier

            password (str): resource owner's Secret

            scope(str, optional): String value of the different scopes the client is asking for.
            Multiple scopes are separated with whitespace.

            realm (str, optional): String value of the realm the user belongs.
            Set this if you want to add realm support at this grant.

            audience (str, optional): The unique identifier of the target API you want to access.

            grant_type (str, optional): Denotes the flow you're using. For password realm
            use http://auth0.com/oauth/grant-type/password-realm

            forwarded_for (str, optional): End-user IP as a string value. Set this if you want
            brute-force protection to work in server-side scenarios.
            See https://auth0.com/docs/get-started/authentication-and-authorization-flow/avoid-common-issues-with-resource-owner-password-flow-and-attack-protection

        Returns:
            access_token, id_token
        """

    def refresh_token(self, refresh_token: str, scope: str = "", grant_type: str = "refresh_token"):
        """Calls /oauth/token endpoint with refresh token grant type

        Use this endpoint to refresh an access token, using the refresh token you got during authorization.

        Args:
            refresh_token (str): The refresh token returned from the initial token request.

            scope (str): Use this to limit the scopes of the new access token.
            Multiple scopes are separated with whitespace.

            grant_type (str): Denotes the flow you're using. For refresh token
            use refresh_token

        Returns:
            access_token, id_token
        """

    def passwordless_login(self, username: str, otp: str, realm: str, scope: str, audience: str):
        """Calls /oauth/token endpoint with http://auth0.com/oauth/grant-type/passwordless/otp grant type

        Once the verification code was received, login the user using this endpoint with their
        phone number/email and verification code.

        Args:
            username (str): The user's phone number or email address.

            otp (str): the user's verification code.

            realm (str): use 'sms' or 'email'.
            Should be the same as the one used to start the passwordless flow.

            scope(str): String value of the different scopes the client is asking for.
            Multiple scopes are separated with whitespace.

            audience (str): The unique identifier of the target API you want to access.

        Returns:
            access_token, id_token
        """

    def backchannel_login(self, auth_req_id: str, grant_type: str = "urn:openid:params:grant-type:ciba"):
        """Calls /oauth/token endpoint with "urn:openid:params:grant-type:ciba" grant type

        Args:
            auth_req_id (str): The id received from /bc-authorize

            grant_type (str): Denotes the flow you're using.For Back Channel login
            use urn:openid:params:grant-type:ciba

        Returns:
            access_token, id_token
        """

    def access_token_for_connection(
        self,
        subject_token_type: str,
        subject_token: str,
        requested_token_type: str,
        connection: str | None = None,
        grant_type: str = ...,
    ):
        """Calls /oauth/token endpoint with federated-connection-access-token grant type

        Args:
            subject_token_type (str): String containing the type of token.

            subject_token (str): String containing the value of subject_token_type.

            requested_token_type (str): String containing the type of rquested token.

            connection (str, optional): Denotes the name of a social identity provider configured to your application

        Returns:
            access_token, scope, issued_token_type, token_type
        """
