from _typeshed import Incomplete
from collections.abc import Mapping
from typing import Any

from authlib.jose import BaseClaims

class ClientMetadataClaims(BaseClaims):
    def validate(self) -> None: ...
    def validate_redirect_uris(self) -> None:
        """Array of redirection URI strings for use in redirect-based flows
        such as the authorization code and implicit flows.  As required by
        Section 2 of OAuth 2.0 [RFC6749], clients using flows with
        redirection MUST register their redirection URI values.
        Authorization servers that support dynamic registration for
        redirect-based flows MUST implement support for this metadata
        value.
        """

    def validate_token_endpoint_auth_method(self) -> None:
        """String indicator of the requested authentication method for the
        token endpoint.
        """

    def validate_grant_types(self) -> None:
        """Array of OAuth 2.0 grant type strings that the client can use at
        the token endpoint.
        """

    def validate_response_types(self) -> None:
        """Array of the OAuth 2.0 response type strings that the client can
        use at the authorization endpoint.
        """

    def validate_client_name(self) -> None:
        """Human-readable string name of the client to be presented to the
        end-user during authorization.  If omitted, the authorization
        server MAY display the raw "client_id" value to the end-user
        instead.  It is RECOMMENDED that clients always send this field.
        The value of this field MAY be internationalized, as described in
        Section 2.2.
        """

    def validate_client_uri(self) -> None:
        """URL string of a web page providing information about the client.
        If present, the server SHOULD display this URL to the end-user in
        a clickable fashion.  It is RECOMMENDED that clients always send
        this field.  The value of this field MUST point to a valid web
        page.  The value of this field MAY be internationalized, as
        described in Section 2.2.
        """

    def validate_logo_uri(self) -> None:
        """URL string that references a logo for the client.  If present, the
        server SHOULD display this image to the end-user during approval.
        The value of this field MUST point to a valid image file.  The
        value of this field MAY be internationalized, as described in
        Section 2.2.
        """

    def validate_scope(self) -> None:
        """String containing a space-separated list of scope values (as
        described in Section 3.3 of OAuth 2.0 [RFC6749]) that the client
        can use when requesting access tokens.  The semantics of values in
        this list are service specific.  If omitted, an authorization
        server MAY register a client with a default set of scopes.
        """

    def validate_contacts(self) -> None:
        """Array of strings representing ways to contact people responsible
        for this client, typically email addresses.  The authorization
        server MAY make these contact addresses available to end-users for
        support requests for the client.  See Section 6 for information on
        Privacy Considerations.
        """

    def validate_tos_uri(self) -> None:
        """URL string that points to a human-readable terms of service
        document for the client that describes a contractual relationship
        between the end-user and the client that the end-user accepts when
        authorizing the client.  The authorization server SHOULD display
        this URL to the end-user if it is provided.  The value of this
        field MUST point to a valid web page.  The value of this field MAY
        be internationalized, as described in Section 2.2.
        """

    def validate_policy_uri(self) -> None:
        """URL string that points to a human-readable privacy policy document
        that describes how the deployment organization collects, uses,
        retains, and discloses personal data.  The authorization server
        SHOULD display this URL to the end-user if it is provided.  The
        value of this field MUST point to a valid web page.  The value of
        this field MAY be internationalized, as described in Section 2.2.
        """

    def validate_jwks_uri(self) -> None:
        """URL string referencing the client's JSON Web Key (JWK) Set
        [RFC7517] document, which contains the client's public keys.  The
        value of this field MUST point to a valid JWK Set document.  These
        keys can be used by higher-level protocols that use signing or
        encryption.  For instance, these keys might be used by some
        applications for validating signed requests made to the token
        endpoint when using JWTs for client authentication [RFC7523].  Use
        of this parameter is preferred over the "jwks" parameter, as it
        allows for easier key rotation.  The "jwks_uri" and "jwks"
        parameters MUST NOT both be present in the same request or
        response.
        """

    def validate_jwks(self) -> None:
        """Client's JSON Web Key Set [RFC7517] document value, which contains
        the client's public keys.  The value of this field MUST be a JSON
        object containing a valid JWK Set.  These keys can be used by
        higher-level protocols that use signing or encryption.  This
        parameter is intended to be used by clients that cannot use the
        "jwks_uri" parameter, such as native clients that cannot host
        public URLs.  The "jwks_uri" and "jwks" parameters MUST NOT both
        be present in the same request or response.
        """

    def validate_software_id(self) -> None:
        """A unique identifier string (e.g., a Universally Unique Identifier
        (UUID)) assigned by the client developer or software publisher
        used by registration endpoints to identify the client software to
        be dynamically registered.  Unlike "client_id", which is issued by
        the authorization server and SHOULD vary between instances, the
        "software_id" SHOULD remain the same for all instances of the
        client software.  The "software_id" SHOULD remain the same across
        multiple updates or versions of the same piece of software.  The
        value of this field is not intended to be human readable and is
        usually opaque to the client and authorization server.
        """

    def validate_software_version(self) -> None:
        """A version identifier string for the client software identified by
        "software_id".  The value of the "software_version" SHOULD change
        on any update to the client software identified by the same
        "software_id".  The value of this field is intended to be compared
        using string equality matching and no other comparison semantics
        are defined by this specification.  The value of this field is
        outside the scope of this specification, but it is not intended to
        be human readable and is usually opaque to the client and
        authorization server.  The definition of what constitutes an
        update to client software that would trigger a change to this
        value is specific to the software itself and is outside the scope
        of this specification.
        """

    @classmethod
    def get_claims_options(cls, metadata: Mapping[str, Incomplete]) -> dict[str, Any]:  # dict values are key-dependent
        """Generate claims options validation from Authorization Server metadata."""
