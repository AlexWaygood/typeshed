import requests

class SigV4Auth:
    access_key: str
    secret_key: str
    session_token: str | None
    region: str
    def __init__(self, access_key: str, secret_key: str, session_token: str | None = None, region: str = "us-east-1") -> None: ...
    def add_auth(self, request: requests.PreparedRequest) -> None: ...

def generate_sigv4_auth_request(header_value: str | None = None):
    """Helper function to prepare a AWS API request to subsequently generate a "AWS Signature Version 4" header.

    :param header_value: Vault allows you to require an additional header, X-Vault-AWS-IAM-Server-ID, to be present
        to mitigate against different types of replay attacks. Depending on the configuration of the AWS auth
        backend, providing a argument to this optional parameter may be required.
    :type header_value: str
    :return: A PreparedRequest instance, optionally containing the provided header value under a
        'X-Vault-AWS-IAM-Server-ID' header name pointed to AWS's simple token service with action "GetCallerIdentity"
    :rtype: requests.PreparedRequest
    """
