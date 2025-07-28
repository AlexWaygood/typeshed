from _typeshed import Incomplete

def create_client_assertion_jwt(
    domain: str, client_id: str, client_assertion_signing_key: str, client_assertion_signing_alg: str | None
) -> str:
    """Creates a JWT for the client_assertion field.

    Args:
        domain (str): The domain of your Auth0 tenant
        client_id (str): Your application's client ID
        client_assertion_signing_key (str): Private key used to sign the client assertion JWT
        client_assertion_signing_alg (str, optional): Algorithm used to sign the client assertion JWT (defaults to 'RS256')

    Returns:
        A JWT signed with the `client_assertion_signing_key`.
    """

def add_client_authentication(
    payload: dict[str, Incomplete],
    domain: str,
    client_id: str,
    client_secret: str | None,
    client_assertion_signing_key: str | None,
    client_assertion_signing_alg: str | None,
) -> dict[str, Incomplete]:
    """Adds the client_assertion or client_secret fields to authenticate a payload.

    Args:
        payload (dict): The POST payload that needs additional fields to be authenticated.
        domain (str): The domain of your Auth0 tenant
        client_id (str): Your application's client ID
        client_secret (str, optional): Your application's client secret
        client_assertion_signing_key (str, optional): Private key used to sign the client assertion JWT
        client_assertion_signing_alg (str, optional): Algorithm used to sign the client assertion JWT (defaults to 'RS256')

    Returns:
        A copy of the payload with client authentication fields added.
    """
