from _typeshed import Incomplete

from authlib.oauth1.rfc5849.base_server import BaseServer

class AuthorizationServer(BaseServer):
    TOKEN_RESPONSE_HEADER: Incomplete
    TEMPORARY_CREDENTIALS_METHOD: str
    def create_oauth1_request(self, request) -> None: ...
    def handle_response(self, status_code, payload, headers) -> None: ...
    def handle_error_response(self, error): ...
    def validate_temporary_credentials_request(self, request):
        """Validate HTTP request for temporary credentials."""

    def create_temporary_credentials_response(self, request=None):
        """Validate temporary credentials token request and create response
        for temporary credentials token. Assume the endpoint of temporary
        credentials request is ``https://photos.example.net/initiate``:

        .. code-block:: http

            POST /initiate HTTP/1.1
            Host: photos.example.net
            Authorization: OAuth realm="Photos",
                oauth_consumer_key="dpf43f3p2l4k3l03",
                oauth_signature_method="HMAC-SHA1",
                oauth_timestamp="137131200",
                oauth_nonce="wIjqoS",
                oauth_callback="http%3A%2F%2Fprinter.example.com%2Fready",
                oauth_signature="74KNZJeDHnMBp0EMJ9ZHt%2FXKycU%3D"

        The server validates the request and replies with a set of temporary
        credentials in the body of the HTTP response:

        .. code-block:: http

            HTTP/1.1 200 OK
            Content-Type: application/x-www-form-urlencoded

            oauth_token=hh5s93j4hdidpola&oauth_token_secret=hdhd0244k9j7ao03&
            oauth_callback_confirmed=true

        :param request: OAuth1Request instance.
        :returns: (status_code, body, headers)
        """

    def validate_authorization_request(self, request):
        """Validate the request for resource owner authorization."""

    def create_authorization_response(self, request, grant_user=None):
        """Validate authorization request and create authorization response.
        Assume the endpoint for authorization request is
        ``https://photos.example.net/authorize``, the client redirects Jane's
        user-agent to the server's Resource Owner Authorization endpoint to
        obtain Jane's approval for accessing her private photos::

            https://photos.example.net/authorize?oauth_token=hh5s93j4hdidpola

        The server requests Jane to sign in using her username and password
        and if successful, asks her to approve granting 'printer.example.com'
        access to her private photos.  Jane approves the request and her
        user-agent is redirected to the callback URI provided by the client
        in the previous request (line breaks are for display purposes only)::

            http://printer.example.com/ready?
            oauth_token=hh5s93j4hdidpola&oauth_verifier=hfdp7dh39dks9884

        :param request: OAuth1Request instance.
        :param grant_user: if granted, pass the grant user, otherwise None.
        :returns: (status_code, body, headers)
        """

    def validate_token_request(self, request):
        """Validate request for issuing token."""

    def create_token_response(self, request):
        """Validate token request and create token response. Assuming the
        endpoint of token request is ``https://photos.example.net/token``,
        the callback request informs the client that Jane completed the
        authorization process.  The client then requests a set of token
        credentials using its temporary credentials (over a secure Transport
        Layer Security (TLS) channel):

        .. code-block:: http

            POST /token HTTP/1.1
            Host: photos.example.net
            Authorization: OAuth realm="Photos",
                oauth_consumer_key="dpf43f3p2l4k3l03",
                oauth_token="hh5s93j4hdidpola",
                oauth_signature_method="HMAC-SHA1",
                oauth_timestamp="137131201",
                oauth_nonce="walatlh",
                oauth_verifier="hfdp7dh39dks9884",
                oauth_signature="gKgrFCywp7rO0OXSjdot%2FIHF7IU%3D"

        The server validates the request and replies with a set of token
        credentials in the body of the HTTP response:

        .. code-block:: http

            HTTP/1.1 200 OK
            Content-Type: application/x-www-form-urlencoded

            oauth_token=nnch734d00sl2jdk&oauth_token_secret=pfkkdhi9sl3r4s00

        :param request: OAuth1Request instance.
        :returns: (status_code, body, headers)
        """

    def create_temporary_credential(self, request) -> None:
        """Generate and save a temporary credential into database or cache.
        A temporary credential is used for exchanging token credential. This
        method should be re-implemented::

            def create_temporary_credential(self, request):
                oauth_token = generate_token(36)
                oauth_token_secret = generate_token(48)
                temporary_credential = TemporaryCredential(
                    oauth_token=oauth_token,
                    oauth_token_secret=oauth_token_secret,
                    client_id=request.client_id,
                    redirect_uri=request.redirect_uri,
                )
                # if the credential has a save method
                temporary_credential.save()
                return temporary_credential

        :param request: OAuth1Request instance
        :return: TemporaryCredential instance
        """

    def get_temporary_credential(self, request) -> None:
        """Get the temporary credential from database or cache. A temporary
        credential should share the same methods as described in models of
        ``TemporaryCredentialMixin``::

            def get_temporary_credential(self, request):
                key = "a-key-prefix:{}".format(request.token)
                data = cache.get(key)
                # TemporaryCredential shares methods from TemporaryCredentialMixin
                return TemporaryCredential(data)

        :param request: OAuth1Request instance
        :return: TemporaryCredential instance
        """

    def delete_temporary_credential(self, request) -> None:
        """Delete temporary credential from database or cache. For instance,
        if temporary credential is saved in cache::

            def delete_temporary_credential(self, request):
                key = "a-key-prefix:{}".format(request.token)
                cache.delete(key)

        :param request: OAuth1Request instance
        """

    def create_authorization_verifier(self, request) -> None:
        """Create and bind ``oauth_verifier`` to temporary credential. It
        could be re-implemented in this way::

            def create_authorization_verifier(self, request):
                verifier = generate_token(36)

                temporary_credential = request.credential
                user_id = request.user.id

                temporary_credential.user_id = user_id
                temporary_credential.oauth_verifier = verifier
                # if the credential has a save method
                temporary_credential.save()

                # remember to return the verifier
                return verifier

        :param request: OAuth1Request instance
        :return: A string of ``oauth_verifier``
        """

    def create_token_credential(self, request) -> None:
        """Create and save token credential into database. This method would
        be re-implemented like this::

            def create_token_credential(self, request):
                oauth_token = generate_token(36)
                oauth_token_secret = generate_token(48)
                temporary_credential = request.credential

                token_credential = TokenCredential(
                    oauth_token=oauth_token,
                    oauth_token_secret=oauth_token_secret,
                    client_id=temporary_credential.get_client_id(),
                    user_id=temporary_credential.get_user_id(),
                )
                # if the credential has a save method
                token_credential.save()
                return token_credential

        :param request: OAuth1Request instance
        :return: TokenCredential instance
        """
