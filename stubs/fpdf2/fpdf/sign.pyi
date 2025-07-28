"""
Module dedicated to document signature generation.

The contents of this module are internal to fpdf2, and not part of the public API.
They may change at any time without prior warning or any deprecation period,
in non-backward-compatible ways.
"""

from _typeshed import Incomplete

class Signature:
    type: str
    filter: str
    sub_filter: str
    contact_info: Incomplete | None
    location: Incomplete | None
    m: Incomplete | None
    reason: Incomplete | None
    byte_range: str
    contents: str
    def __init__(self, contact_info=None, location=None, m=None, reason=None) -> None: ...
    def serialize(self) -> str: ...

def sign_content(signer, buffer, key, cert, extra_certs, hashalgo, sign_time):
    """
    Perform PDF signing based on the content of the buffer, performing substitutions on it.
    The signing operation does not alter the buffer size
    """
