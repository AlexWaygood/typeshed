"""PKI methods module."""

from hvac.api.vault_api_base import VaultApiBase

DEFAULT_MOUNT_POINT: str

class Pki(VaultApiBase):
    """Pki Secrets Engine (API).

    Reference: https://www.vaultproject.io/api/secret/pki/index.html
    """

    def read_ca_certificate(self, mount_point="pki"):
        """Read CA Certificate.

        Retrieves the CA certificate in raw DER-encoded form.

        Supported methods:
            GET: /{mount_point}/ca/pem. Produces: String

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The certificate as pem.
        :rtype: str
        """

    def read_ca_certificate_chain(self, mount_point="pki"):
        """Read CA Certificate Chain.

        Retrieves the CA certificate chain, including the CA in PEM format.

        Supported methods:
            GET: /{mount_point}/ca_chain. Produces: String

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The certificate chain as pem.
        :rtype: str
        """

    def read_certificate(self, serial, mount_point="pki"):
        """Read Certificate.

        Retrieves one of a selection of certificates.

        Supported methods:
            GET: /{mount_point}/cert/{serial}. Produces: 200 application/json

        :param serial: the serial of the key to read.
        :type serial: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: dict
        """

    def list_certificates(self, mount_point="pki"):
        """List Certificates.

        The list of the current certificates by serial number only.

        Supported methods:
            LIST: /{mount_point}/certs. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: dict
        """

    def submit_ca_information(self, pem_bundle, mount_point="pki"):
        """Submit CA Information.

        Submitting the CA information for the backend.

        Supported methods:
            POST: /{mount_point}/config/ca. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def read_crl_configuration(self, mount_point="pki"):
        """Read CRL Configuration.

        Getting the duration for which the generated CRL should be marked valid.

        Supported methods:
            GET: /{mount_point}/config/crl. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: dict
        """

    def set_crl_configuration(self, expiry=None, disable=None, extra_params=None, mount_point="pki"):
        """Set CRL Configuration.

        Setting the duration for which the generated CRL should be marked valid.
        If the CRL is disabled, it will return a signed but zero-length CRL for any
        request. If enabled, it will re-build the CRL.

        Supported methods:
            POST: /{mount_point}/config/crl. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def read_urls(self, mount_point="pki"):
        """Read URLs.

        Fetches the URLs to be encoded in generated certificates.

        Supported methods:
            GET: /{mount_point}/config/urls. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: dict
        """

    def set_urls(self, params, mount_point="pki"):
        """Set URLs.

        Setting the issuing certificate endpoints, CRL distribution points, and OCSP server endpoints that will be
        encoded into issued certificates. You can update any of the values at any time without affecting the other
        existing values. To remove the values, simply use a blank string as the parameter.

        Supported methods:
            POST: /{mount_point}/config/urls. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def read_crl(self, mount_point="pki"):
        """Read CRL.

        Retrieves the current CRL in PEM format.
        This endpoint is an unauthenticated.

        Supported methods:
            GET: /{mount_point}/crl/pem. Produces: 200 application/pkix-crl

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The content of the request e.g. CRL string representation.
        :rtype: str
        """

    def rotate_crl(self, mount_point="pki"):
        """Rotate CRLs.

        Forces a rotation of the CRL.

        Supported methods:
            GET: /{mount_point}/crl/rotate. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: dict
        """

    def generate_intermediate(self, type, common_name, extra_params=None, mount_point="pki", wrap_ttl=None):
        """Generate Intermediate.

        Generates a new private key and a CSR for signing.

        Supported methods:
            POST: /{mount_point}/intermediate/generate/{type}. Produces: 200 application/json

        :param type: Specifies the type to create. `exported` (private key also exported) or `internal`.
        :type type: str | unicode
        :param common_name: Specifies the requested CN for the certificate.
        :type common_name: str | unicode
        :param extra_params: Dictionary with extra parameters.
        :type extra_params: dict
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :param wrap_ttl: Specifies response wrapping token creation with duration. IE: '15s', '20m', '25h'.
        :type wrap_ttl: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def set_signed_intermediate(self, certificate, mount_point="pki"):
        """Set Signed Intermediate.

        Allows submitting the signed CA certificate corresponding to a private key generated via "Generate Intermediate"

        Supported methods:
            POST: /{mount_point}/intermediate/set-signed. Produces: 200 application/json

        :param certificate: Specifies the certificate in PEM format.
        :type certificate: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def generate_certificate(self, name, common_name, extra_params=None, mount_point="pki", wrap_ttl=None):
        """Generate Certificate.

        Generates a new set of credentials (private key and certificate) based on the role named in the endpoint.

        Supported methods:
            POST: /{mount_point}/issue/{name}. Produces: 200 application/json

        :param name: The name of the role to create the certificate against.
        :name name: str | unicode
        :param common_name: The requested CN for the certificate.
        :name common_name: str | unicode
        :param extra_params: A dictionary with extra parameters.
        :name extra_params: dict
        :param mount_point: The "path" the method/backend was mounted on.
        :name mount_point: str | unicode
        :param wrap_ttl: Specifies response wrapping token creation with duration. IE: '15s', '20m', '25h'.
        :type wrap_ttl: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def revoke_certificate(self, serial_number, mount_point="pki"):
        """Revoke Certificate.

        Revokes a certificate using its serial number.

        Supported methods:
            POST: /{mount_point}/revoke. Produces: 200 application/json

        :param serial_number: The serial number of the certificate to revoke.
        :name serial_number: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :name mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def create_or_update_role(self, name, extra_params=None, mount_point="pki"):
        """Create/Update Role.

        Creates or updates the role definition.

        Supported methods:
            POST: /{mount_point}/roles/{name}. Produces: 200 application/json

        :param name: The name of the role to create.
        :name name: str | unicode
        :param extra_params: A dictionary with extra parameters.
        :name extra_params: dict
        :param mount_point: The "path" the method/backend was mounted on.
        :name mount_point: str | unicode
        :return: The JSON response of the request.
        :rname: requests.Response
        """

    def read_role(self, name, mount_point="pki"):
        """Read Role.

        Queries the role definition.

        Supported methods:
            GET: /{mount_point}/roles/{name}. Produces: 200 application/json

        :param name: The name of the role to read.
        :type name: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: dict
        """

    def list_roles(self, mount_point="pki"):
        """List Roles.

        Get a list of available roles.

        Supported methods:
            LIST: /{mount_point}/roles. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: dict
        """

    def delete_role(self, name, mount_point="pki"):
        """Delete Role.

        Deletes the role definition.

        Supported methods:
            DELETE: /{mount_point}/roles/{name}. Produces: 200 application/json

        :param name: The name of the role to delete.
        :name name: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :name mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def generate_root(self, type, common_name, extra_params=None, mount_point="pki", wrap_ttl=None):
        """Generate Root.

        Generates a new self-signed CA certificate and private key.

        Supported methods:
            POST: /{mount_point}/root/generate/{type}. Produces: 200 application/json

        :param type: Specifies the type to create. `exported` (private key also exported) or `internal`.
        :type type: str | unicode
        :param common_name: The requested CN for the certificate.
        :type common_name: str | unicode
        :param extra_params: A dictionary with extra parameters.
        :type extra_params: dict
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :param wrap_ttl: Specifies response wrapping token creation with duration. IE: '15s', '20m', '25h'.
        :type wrap_ttl: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def delete_root(self, mount_point="pki"):
        """Delete Root.

        Deletes the current CA key.

        Supported methods:
            DELETE: /{mount_point}/root. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def sign_intermediate(self, csr, common_name, extra_params=None, mount_point="pki"):
        """Sign Intermediate.

        Issue a certificate with appropriate values for acting as an intermediate CA.

        Supported methods:
            POST: /{mount_point}/root/sign-intermediate. Produces: 200 application/json

        :param csr: The PEM-encoded CSR.
        :type csr: str | unicode
        :param common_name: The requested CN for the certificate.
        :type common_name: str | unicode
        :param extra_params: Dictionary with extra parameters.
        :type extra_params: dict
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def sign_self_issued(self, certificate, mount_point="pki"):
        """Sign Self-Issued.

        Sign a self-issued certificate.

        Supported methods:
            POST: /{mount_point}/root/sign-self-issued. Produces: 200 application/json

        :param certificate: The PEM-encoded self-issued certificate.
        :type certificate: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def sign_certificate(self, name, csr, common_name, extra_params=None, mount_point="pki"):
        """Sign Certificate.

        Signs a new certificate based upon the provided CSR and the supplied parameters.

        Supported methods:
            POST: /{mount_point}/sign/{name}. Produces: 200 application/json

        :param name: The role to sign the certificate.
        :type name: str | unicode
        :param csr: The PEM-encoded CSR.
        :type csr: str | unicode
        :param common_name: The requested CN for the certificate. If the CN is allowed by role policy, it will be issued.
        :type common_name: str | unicode
        :param extra_params: A dictionary with extra parameters.
        :type extra_params: dict
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def sign_verbatim(self, csr, name: bool = False, extra_params=None, mount_point="pki"):
        """Sign Verbatim.

        Signs a new certificate based upon the provided CSR.

        Supported methods:
            POST: /{mount_point}/sign-verbatim. Produces: 200 application/json

        :param csr: The PEM-encoded CSR.
        :type csr: str | unicode
        :param name: Specifies a role.
        :type name: str | unicode
        :param extra_params: A dictionary with extra parameters.
        :type extra_params: dict
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def tidy(self, extra_params=None, mount_point="pki"):
        """Tidy.

        Allows tidying up the storage backend and/or CRL by removing certificates that have
        expired and are past a certain buffer period beyond their expiration time.

        Supported methods:
            POST: /{mount_point}/tidy. Produces: 200 application/json

        :param extra_params: A dictionary with extra parameters.
        :type extra_params: dict
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def read_issuer(self, issuer_ref, mount_point="pki"):
        """Read issuer.

        Get configuration of a issuer by its reference ID.

        Supported methods:
            GET: /{mount_point}/issuer/{issuer_ref}. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :param issuer_ref: The reference ID of the issuer to get
        :type issuer_ref: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def list_issuers(self, mount_point="pki"):
        """List issuers.

        Get list of all issuers for a given pki mount.

        Supported methods:
            LIST: /{mount_point}/issuers. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def update_issuer(self, issuer_ref, extra_params=None, mount_point="pki"):
        """Update issuer.

        Update a given issuer.

        Supported methods:
            POST: /{mount_point}/issuer/{issuer_ref}. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :param issuer_ref: The reference ID of the issuer to update
        :type issuer_ref: str | unicode
        :param extra_params: Dictionary with extra parameters.
        :type extra_params: dict
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def revoke_issuer(self, issuer_ref, mount_point="pki"):
        """Revoke issuer.

        Revokes a given issuer.

        Supported methods:
            POST: /{mount_point}/issuer/{issuer_ref}/revoke. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :param issuer_ref: The reference ID of the issuer to revoke
        :type issuer_ref: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """

    def delete_issuer(self, issuer_ref, mount_point="pki"):
        """Delete issuer.

        Delete a given issuer. Deleting the default issuer will result in a warning

        Supported methods:
            DELETE: /{mount_point}/issuer/{issuer_ref}. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :param issuer_ref: The reference ID of the issuer to delete
        :type issuer_ref: str | unicode
        :return: The JSON response of the request.
        :rtype: requests.Response
        """
