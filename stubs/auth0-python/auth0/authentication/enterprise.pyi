from .base import AuthenticationBase

class Enterprise(AuthenticationBase):
    """Enterprise endpoints.

    Args:
        domain (str): Your auth0 domain (e.g: my-domain.us.auth0.com)
    """

    def saml_metadata(self):
        """Get SAML2.0 Metadata."""

    def wsfed_metadata(self):
        """Returns the WS-Federation Metadata."""
