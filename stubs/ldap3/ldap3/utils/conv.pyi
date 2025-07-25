""" """

def to_unicode(obj: float | bytes | str, encoding: str | None = None, from_server: bool = False) -> str:
    """Try to convert bytes (and str in python2) to unicode.
    Return object unmodified if python3 string, else raise an exception
    """

def to_raw(obj, encoding: str = "utf-8"):
    """Tries to convert to raw bytes from unicode"""

def escape_filter_chars(text: float | bytes | str, encoding: str | None = None) -> str:
    """Escape chars mentioned in RFC4515."""

def unescape_filter_chars(text, encoding=None):
    """unescape chars mentioned in RFC4515."""

def escape_bytes(bytes_value: str | bytes) -> str:
    """Convert a byte sequence to a properly escaped for LDAP (format BACKSLASH HEX HEX) string"""

def prepare_for_stream(value): ...
def json_encode_b64(obj): ...
def check_json_dict(json_dict) -> None: ...
def json_hook(obj): ...
def format_json(obj, iso_format: bool = False): ...
def is_filter_escaped(text): ...
def ldap_escape_to_bytes(text): ...
