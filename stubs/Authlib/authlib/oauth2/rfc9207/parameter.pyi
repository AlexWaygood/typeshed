class IssuerParameter:
    def __call__(self, authorization_server) -> None: ...
    def add_issuer_parameter(self, authorization_server, response) -> None: ...
    def get_issuer(self) -> str | None:
        """Return the issuer URL.
        Developers MAY implement this method if they want to support :rfc:`RFC9207 <9207>`::

            def get_issuer(self) -> str:
                return "https://auth.example.org"
        """
