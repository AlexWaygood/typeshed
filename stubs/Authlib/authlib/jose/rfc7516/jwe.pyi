from _typeshed import Incomplete

class JsonWebEncryption:
    REGISTERED_HEADER_PARAMETER_NAMES: Incomplete
    ALG_REGISTRY: Incomplete
    ENC_REGISTRY: Incomplete
    ZIP_REGISTRY: Incomplete
    def __init__(self, algorithms=None, private_headers=None) -> None: ...
    @classmethod
    def register_algorithm(cls, algorithm) -> None:
        """Register an algorithm for ``alg`` or ``enc`` or ``zip`` of JWE."""

    def serialize_compact(self, protected, payload, key, sender_key=None):
        """Generate a JWE Compact Serialization.

        The JWE Compact Serialization represents encrypted content as a compact,
        URL-safe string. This string is::

            BASE64URL(UTF8(JWE Protected Header)) || '.' ||
            BASE64URL(JWE Encrypted Key) || '.' ||
            BASE64URL(JWE Initialization Vector) || '.' ||
            BASE64URL(JWE Ciphertext) || '.' ||
            BASE64URL(JWE Authentication Tag)

        Only one recipient is supported by the JWE Compact Serialization and
        it provides no syntax to represent JWE Shared Unprotected Header, JWE
        Per-Recipient Unprotected Header, or JWE AAD values.

        :param protected: A dict of protected header
        :param payload: Payload (bytes or a value convertible to bytes)
        :param key: Public key used to encrypt payload
        :param sender_key: Sender's private key in case
            JWEAlgorithmWithTagAwareKeyAgreement is used
        :return: JWE compact serialization as bytes
        """

    def serialize_json(self, header_obj, payload, keys, sender_key=None):
        """Generate a JWE JSON Serialization (in fully general syntax).

        The JWE JSON Serialization represents encrypted content as a JSON
        object.  This representation is neither optimized for compactness nor
        URL safe.

        The following members are defined for use in top-level JSON objects
        used for the fully general JWE JSON Serialization syntax:

        protected
            The "protected" member MUST be present and contain the value
            BASE64URL(UTF8(JWE Protected Header)) when the JWE Protected
            Header value is non-empty; otherwise, it MUST be absent.  These
            Header Parameter values are integrity protected.

        unprotected
            The "unprotected" member MUST be present and contain the value JWE
            Shared Unprotected Header when the JWE Shared Unprotected Header
            value is non-empty; otherwise, it MUST be absent.  This value is
            represented as an unencoded JSON object, rather than as a string.
            These Header Parameter values are not integrity protected.

        iv
            The "iv" member MUST be present and contain the value
            BASE64URL(JWE Initialization Vector) when the JWE Initialization
            Vector value is non-empty; otherwise, it MUST be absent.

        aad
            The "aad" member MUST be present and contain the value
            BASE64URL(JWE AAD)) when the JWE AAD value is non-empty;
            otherwise, it MUST be absent.  A JWE AAD value can be included to
            supply a base64url-encoded value to be integrity protected but not
            encrypted.

        ciphertext
            The "ciphertext" member MUST be present and contain the value
            BASE64URL(JWE Ciphertext).

        tag
            The "tag" member MUST be present and contain the value
            BASE64URL(JWE Authentication Tag) when the JWE Authentication Tag
            value is non-empty; otherwise, it MUST be absent.

        recipients
            The "recipients" member value MUST be an array of JSON objects.
            Each object contains information specific to a single recipient.
            This member MUST be present with exactly one array element per
            recipient, even if some or all of the array element values are the
            empty JSON object "{}" (which can happen when all Header Parameter
            values are shared between all recipients and when no encrypted key
            is used, such as when doing Direct Encryption).

        The following members are defined for use in the JSON objects that
        are elements of the "recipients" array:

        header
            The "header" member MUST be present and contain the value JWE Per-
            Recipient Unprotected Header when the JWE Per-Recipient
            Unprotected Header value is non-empty; otherwise, it MUST be
            absent.  This value is represented as an unencoded JSON object,
            rather than as a string.  These Header Parameter values are not
            integrity protected.

        encrypted_key
            The "encrypted_key" member MUST be present and contain the value
            BASE64URL(JWE Encrypted Key) when the JWE Encrypted Key value is
            non-empty; otherwise, it MUST be absent.

        This implementation assumes that "alg" and "enc" header fields are
        contained in the protected or shared unprotected header.

        :param header_obj: A dict of headers (in addition optionally contains JWE AAD)
        :param payload: Payload (bytes or a value convertible to bytes)
        :param keys: Public keys (or a single public key) used to encrypt payload
        :param sender_key: Sender's private key in case
            JWEAlgorithmWithTagAwareKeyAgreement is used
        :return: JWE JSON serialization (in fully general syntax) as dict

        Example of `header_obj`::

            {
                "protected": {
                    "alg": "ECDH-1PU+A128KW",
                    "enc": "A256CBC-HS512",
                    "apu": "QWxpY2U",
                    "apv": "Qm9iIGFuZCBDaGFybGll",
                },
                "unprotected": {"jku": "https://alice.example.com/keys.jwks"},
                "recipients": [
                    {"header": {"kid": "bob-key-2"}},
                    {"header": {"kid": "2021-05-06"}},
                ],
                "aad": b"Authenticate me too.",
            }
        """

    def serialize(self, header, payload, key, sender_key=None):
        """Generate a JWE Serialization.

        It will automatically generate a compact or JSON serialization depending
        on `header` argument. If `header` is a dict with "protected",
        "unprotected" and/or "recipients" keys, it will call `serialize_json`,
        otherwise it will call `serialize_compact`.

        :param header: A dict of header(s)
        :param payload: Payload (bytes or a value convertible to bytes)
        :param key: Public key(s) used to encrypt payload
        :param sender_key: Sender's private key in case
            JWEAlgorithmWithTagAwareKeyAgreement is used
        :return: JWE compact serialization as bytes or
            JWE JSON serialization as dict
        """

    def deserialize_compact(self, s, key, decode=None, sender_key=None):
        """Extract JWE Compact Serialization.

        :param s: JWE Compact Serialization as bytes
        :param key: Private key used to decrypt payload
            (optionally can be a tuple of kid and essentially key)
        :param decode: Function to decode payload data
        :param sender_key: Sender's public key in case
            JWEAlgorithmWithTagAwareKeyAgreement is used
        :return: dict with `header` and `payload` keys where `header` value is
            a dict containing protected header fields
        """

    def deserialize_json(self, obj, key, decode=None, sender_key=None):
        """Extract JWE JSON Serialization.

        :param obj: JWE JSON Serialization as dict or str
        :param key: Private key used to decrypt payload
            (optionally can be a tuple of kid and essentially key)
        :param decode: Function to decode payload data
        :param sender_key: Sender's public key in case
            JWEAlgorithmWithTagAwareKeyAgreement is used
        :return: dict with `header` and `payload` keys where `header` value is
            a dict containing `protected`, `unprotected`, `recipients` and/or
            `aad` keys
        """

    def deserialize(self, obj, key, decode=None, sender_key=None):
        """Extract a JWE Serialization.

        It supports both compact and JSON serialization.

        :param obj: JWE compact serialization as bytes or
            JWE JSON serialization as dict or str
        :param key: Private key used to decrypt payload
            (optionally can be a tuple of kid and essentially key)
        :param decode: Function to decode payload data
        :param sender_key: Sender's public key in case
            JWEAlgorithmWithTagAwareKeyAgreement is used
        :return: dict with `header` and `payload` keys
        """

    @staticmethod
    def parse_json(obj):
        """Parse JWE JSON Serialization.

        :param obj: JWE JSON Serialization as str or dict
        :return: Parsed JWE JSON Serialization as dict if `obj` is an str,
            or `obj` as is if `obj` is already a dict
        """

    def get_header_alg(self, header): ...
    def get_header_enc(self, header): ...
    def get_header_zip(self, header): ...

def prepare_key(alg, header, key): ...
