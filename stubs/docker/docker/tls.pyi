from docker import APIClient

class TLSConfig:
    """
    TLS configuration.

    Args:
        client_cert (tuple of str): Path to client cert, path to client key.
        ca_cert (str): Path to CA cert file.
        verify (bool or str): This can be a bool or a path to a CA cert
            file to verify against. If ``True``, verify using ca_cert;
            if ``False`` or not specified, do not verify.
    """

    cert: tuple[str, str] | None
    ca_cert: str | None
    verify: bool | str | None
    def __init__(
        self, client_cert: tuple[str, str] | None = None, ca_cert: str | None = None, verify: bool | str | None = None
    ) -> None: ...
    def configure_client(self, client: APIClient) -> None:
        """
        Configure a client with these TLS options.
        """
