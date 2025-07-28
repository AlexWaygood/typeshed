"""
Regex for URIs

These regex are directly derived from the collected ABNF in RFC3986
(except for DIGIT, ALPHA and HEXDIG, defined by RFC2234).

They should be processed with re.VERBOSE.

Thanks Mark Nottingham for this code - https://gist.github.com/138549
"""

import re
from typing import Final

DIGIT: Final[str]
ALPHA: Final[str]
HEXDIG: Final[str]
pct_encoded: Final[str]
unreserved: Final[str]
gen_delims: Final[str]
sub_delims: Final[str]
pchar: Final[str]
reserved: Final[str]
scheme: Final[str]
dec_octet: Final[str]
IPv4address: Final[str]
IPv6address: Final[str]
IPvFuture: Final[str]
IP_literal: Final[str]
reg_name: Final[str]
userinfo: Final[str]
host: Final[str]
port: Final[str]
authority: Final[str]
segment: Final[str]
segment_nz: Final[str]
segment_nz_nc: Final[str]
path_abempty: Final[str]
path_absolute: Final[str]
path_noscheme: Final[str]
path_rootless: Final[str]
path_empty: Final[str]
path: Final[str]
query: Final[str]
fragment: Final[str]
hier_part: Final[str]
relative_part: Final[str]
relative_ref: Final[str]
URI: Final[str]
URI_reference: Final[str]
absolute_URI: Final[str]

def is_uri(uri: str) -> re.Match[str] | None: ...
def is_uri_reference(uri: str) -> re.Match[str] | None: ...
def is_absolute_uri(uri: str) -> re.Match[str] | None: ...
