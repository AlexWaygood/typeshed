from _typeshed import Incomplete

CONTENT_TYPE_FORM_URLENCODED: str
CONTENT_TYPE_MULTI_PART: str

class ClientAuth:
    SIGNATURE_METHODS: Incomplete
    @classmethod
    def register_signature_method(cls, name, sign) -> None:
        """Extend client signature methods.

        :param name: A string to represent signature method.
        :param sign: A function to generate signature.

        The ``sign`` method accept 2 parameters::

            def custom_sign_method(client, request):
                # client is the instance of Client.
                return "your-signed-string"


            Client.register_signature_method("custom-name", custom_sign_method)
        """
    client_id: Incomplete
    client_secret: Incomplete
    token: Incomplete
    token_secret: Incomplete
    redirect_uri: Incomplete
    signature_method: Incomplete
    signature_type: Incomplete
    rsa_key: Incomplete
    verifier: Incomplete
    realm: Incomplete
    force_include_body: Incomplete
    def __init__(
        self,
        client_id,
        client_secret=None,
        token=None,
        token_secret=None,
        redirect_uri=None,
        rsa_key=None,
        verifier=None,
        signature_method="HMAC-SHA1",
        signature_type="HEADER",
        realm=None,
        force_include_body: bool = False,
    ) -> None: ...
    def get_oauth_signature(self, method, uri, headers, body):
        """Get an OAuth signature to be used in signing a request.

        To satisfy `section 3.4.1.2`_ item 2, if the request argument's
        headers dict attribute contains a Host item, its value will
        replace any netloc part of the request argument's uri attribute
        value.

        .. _`section 3.4.1.2`: https://tools.ietf.org/html/rfc5849#section-3.4.1.2
        """

    def get_oauth_params(self, nonce, timestamp): ...
    def sign(self, method, uri, headers, body):
        """Sign the HTTP request, add OAuth parameters and signature.

        :param method: HTTP method of the request.
        :param uri:  URI of the HTTP request.
        :param body: Body payload of the HTTP request.
        :param headers: Headers of the HTTP request.
        :return: uri, headers, body
        """

    def prepare(self, method, uri, headers, body):
        """Add OAuth parameters to the request.

        Parameters may be included from the body if the content-type is
        urlencoded, if no content type is set, a guess is made.
        """

def generate_nonce(): ...
def generate_timestamp(): ...
