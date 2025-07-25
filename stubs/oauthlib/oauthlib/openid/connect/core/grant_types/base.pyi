from _hashlib import HASH
from collections.abc import Callable
from logging import Logger

from oauthlib.common import Request

log: Logger

class GrantTypeBase:
    def __getattr__(self, attr: str): ...
    def __setattr__(self, attr: str, value) -> None: ...
    def validate_authorization_request(self, request: Request):
        """Validates the OpenID Connect authorization request parameters.

        :returns: (list of scopes, dict of request info)
        """

    def id_token_hash(
        self, value: str, hashfunc: Callable[..., HASH] = ...  # Arguments: ReadableBuffer (string) and bool (usedforsecurity)
    ) -> str:
        """
        Its value is the base64url encoding of the left-most half of the
        hash of the octets of the ASCII representation of the access_token
        value, where the hash algorithm used is the hash algorithm used in
        the alg Header Parameter of the ID Token's JOSE Header.

        For instance, if the alg is RS256, hash the access_token value
        with SHA-256, then take the left-most 128 bits and
        base64url-encode them.
        For instance, if the alg is HS512, hash the code value with
        SHA-512, then take the left-most 256 bits and base64url-encode
        them. The c_hash value is a case-sensitive string.

        Example of hash from OIDC specification (bound to a JWS using RS256):

        code:
        Qcb0Orv1zh30vL1MPRsbm-diHiMwcLyZvn1arpZv-Jxf_11jnpEX3Tgfvk

        c_hash:
        LDktKdoQak3Pk0cnXxCltA
        """

    def add_id_token(self, token, token_handler, request: Request, nonce=None):
        """
        Construct an initial version of id_token, and let the
        request_validator sign or encrypt it.

        The initial version can contain the fields below, accordingly
        to the spec:
        - aud
        - iat
        - nonce
        - at_hash
        - c_hash
        """

    def openid_authorization_validator(self, request: Request):
        """Perform OpenID Connect specific authorization request validation.

        nonce
                OPTIONAL. String value used to associate a Client session with
                an ID Token, and to mitigate replay attacks. The value is
                passed through unmodified from the Authentication Request to
                the ID Token. Sufficient entropy MUST be present in the nonce
                values used to prevent attackers from guessing values

        display
                OPTIONAL. ASCII string value that specifies how the
                Authorization Server displays the authentication and consent
                user interface pages to the End-User. The defined values are:

                    page - The Authorization Server SHOULD display the
                    authentication and consent UI consistent with a full User
                    Agent page view. If the display parameter is not specified,
                    this is the default display mode.

                    popup - The Authorization Server SHOULD display the
                    authentication and consent UI consistent with a popup User
                    Agent window. The popup User Agent window should be of an
                    appropriate size for a login-focused dialog and should not
                    obscure the entire window that it is popping up over.

                    touch - The Authorization Server SHOULD display the
                    authentication and consent UI consistent with a device that
                    leverages a touch interface.

                    wap - The Authorization Server SHOULD display the
                    authentication and consent UI consistent with a "feature
                    phone" type display.

                The Authorization Server MAY also attempt to detect the
                capabilities of the User Agent and present an appropriate
                display.

        prompt
                OPTIONAL. Space delimited, case sensitive list of ASCII string
                values that specifies whether the Authorization Server prompts
                the End-User for reauthentication and consent. The defined
                values are:

                    none - The Authorization Server MUST NOT display any
                    authentication or consent user interface pages. An error is
                    returned if an End-User is not already authenticated or the
                    Client does not have pre-configured consent for the
                    requested Claims or does not fulfill other conditions for
                    processing the request. The error code will typically be
                    login_required, interaction_required, or another code
                    defined in Section 3.1.2.6. This can be used as a method to
                    check for existing authentication and/or consent.

                    login - The Authorization Server SHOULD prompt the End-User
                    for reauthentication. If it cannot reauthenticate the
                    End-User, it MUST return an error, typically
                    login_required.

                    consent - The Authorization Server SHOULD prompt the
                    End-User for consent before returning information to the
                    Client. If it cannot obtain consent, it MUST return an
                    error, typically consent_required.

                    select_account - The Authorization Server SHOULD prompt the
                    End-User to select a user account. This enables an End-User
                    who has multiple accounts at the Authorization Server to
                    select amongst the multiple accounts that they might have
                    current sessions for. If it cannot obtain an account
                    selection choice made by the End-User, it MUST return an
                    error, typically account_selection_required.

                The prompt parameter can be used by the Client to make sure
                that the End-User is still present for the current session or
                to bring attention to the request. If this parameter contains
                none with any other value, an error is returned.

        max_age
                OPTIONAL. Maximum Authentication Age. Specifies the allowable
                elapsed time in seconds since the last time the End-User was
                actively authenticated by the OP. If the elapsed time is
                greater than this value, the OP MUST attempt to actively
                re-authenticate the End-User. (The max_age request parameter
                corresponds to the OpenID 2.0 PAPE [OpenID.PAPE] max_auth_age
                request parameter.) When max_age is used, the ID Token returned
                MUST include an auth_time Claim Value.

        ui_locales
                OPTIONAL. End-User's preferred languages and scripts for the
                user interface, represented as a space-separated list of BCP47
                [RFC5646] language tag values, ordered by preference. For
                instance, the value "fr-CA fr en" represents a preference for
                French as spoken in Canada, then French (without a region
                designation), followed by English (without a region
                designation). An error SHOULD NOT result if some or all of the
                requested locales are not supported by the OpenID Provider.

        id_token_hint
                OPTIONAL. ID Token previously issued by the Authorization
                Server being passed as a hint about the End-User's current or
                past authenticated session with the Client. If the End-User
                identified by the ID Token is logged in or is logged in by the
                request, then the Authorization Server returns a positive
                response; otherwise, it SHOULD return an error, such as
                login_required. When possible, an id_token_hint SHOULD be
                present when prompt=none is used and an invalid_request error
                MAY be returned if it is not; however, the server SHOULD
                respond successfully when possible, even if it is not present.
                The Authorization Server need not be listed as an audience of
                the ID Token when it is used as an id_token_hint value. If the
                ID Token received by the RP from the OP is encrypted, to use it
                as an id_token_hint, the Client MUST decrypt the signed ID
                Token contained within the encrypted ID Token. The Client MAY
                re-encrypt the signed ID token to the Authentication Server
                using a key that enables the server to decrypt the ID Token,
                and use the re-encrypted ID token as the id_token_hint value.

        login_hint
                OPTIONAL. Hint to the Authorization Server about the login
                identifier the End-User might use to log in (if necessary).
                This hint can be used by an RP if it first asks the End-User
                for their e-mail address (or other identifier) and then wants
                to pass that value as a hint to the discovered authorization
                service. It is RECOMMENDED that the hint value match the value
                used for discovery. This value MAY also be a phone number in
                the format specified for the phone_number Claim. The use of
                this parameter is left to the OP's discretion.

        acr_values
                OPTIONAL. Requested Authentication Context Class Reference
                values. Space-separated string that specifies the acr values
                that the Authorization Server is being requested to use for
                processing this Authentication Request, with the values
                appearing in order of preference. The Authentication Context
                Class satisfied by the authentication performed is returned as
                the acr Claim Value, as specified in Section 2. The acr Claim
                is requested as a Voluntary Claim by this parameter.
        """

OpenIDConnectBase = GrantTypeBase
