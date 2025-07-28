from _typeshed import Incomplete

class JsonWebSignature:
    REGISTERED_HEADER_PARAMETER_NAMES: Incomplete
    ALGORITHMS_REGISTRY: Incomplete
    def __init__(self, algorithms=None, private_headers=None) -> None: ...
    @classmethod
    def register_algorithm(cls, algorithm) -> None: ...
    def serialize_compact(self, protected, payload, key):
        """Generate a JWS Compact Serialization. The JWS Compact Serialization
        represents digitally signed or MACed content as a compact, URL-safe
        string, per `Section 7.1`_.

        .. code-block:: text

            BASE64URL(UTF8(JWS Protected Header)) || '.' ||
            BASE64URL(JWS Payload) || '.' ||
            BASE64URL(JWS Signature)

        :param protected: A dict of protected header
        :param payload: A bytes/string of payload
        :param key: Private key used to generate signature
        :return: byte
        """

    def deserialize_compact(self, s, key, decode=None):
        """Exact JWS Compact Serialization, and validate with the given key.
        If key is not provided, the returned dict will contain the signature,
        and signing input values. Via `Section 7.1`_.

        :param s: text of JWS Compact Serialization
        :param key: key used to verify the signature
        :param decode: a function to decode payload data
        :return: JWSObject
        :raise: BadSignatureError

        .. _`Section 7.1`: https://tools.ietf.org/html/rfc7515#section-7.1
        """

    def serialize_json(self, header_obj, payload, key):
        """Generate a JWS JSON Serialization. The JWS JSON Serialization
        represents digitally signed or MACed content as a JSON object,
        per `Section 7.2`_.

        :param header_obj: A dict/list of header
        :param payload: A string/dict of payload
        :param key: Private key used to generate signature
        :return: JWSObject

        Example ``header_obj`` of JWS JSON Serialization::

            {
                "protected: {"alg": "HS256"},
                "header": {"kid": "jose"}
            }

        Pass a dict to generate flattened JSON Serialization, pass a list of
        header dict to generate standard JSON Serialization.
        """

    def deserialize_json(self, obj, key, decode=None):
        """Exact JWS JSON Serialization, and validate with the given key.
        If key is not provided, it will return a dict without signature
        verification. Header will still be validated. Via `Section 7.2`_.

        :param obj: text of JWS JSON Serialization
        :param key: key used to verify the signature
        :param decode: a function to decode payload data
        :return: JWSObject
        :raise: BadSignatureError

        .. _`Section 7.2`: https://tools.ietf.org/html/rfc7515#section-7.2
        """

    def serialize(self, header, payload, key):
        """Generate a JWS Serialization. It will automatically generate a
        Compact or JSON Serialization depending on the given header. If a
        header is in a JSON header format, it will call
        :meth:`serialize_json`, otherwise it will call
        :meth:`serialize_compact`.

        :param header: A dict/list of header
        :param payload: A string/dict of payload
        :param key: Private key used to generate signature
        :return: byte/dict
        """

    def deserialize(self, s, key, decode=None):
        """Deserialize JWS Serialization, both compact and JSON format.
        It will automatically deserialize depending on the given JWS.

        :param s: text of JWS Compact/JSON Serialization
        :param key: key used to verify the signature
        :param decode: a function to decode payload data
        :return: dict
        :raise: BadSignatureError

        If key is not provided, it will still deserialize the serialization
        without verification.
        """
