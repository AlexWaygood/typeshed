""" """

STATE_ANY: int
STATE_ESCAPE: int
STATE_ESCAPE_HEX: int

def to_dn(
    iterator, decompose: bool = False, remove_space: bool = False, space_around_equal: bool = False, separate_rdn: bool = False
):
    """
    Convert an iterator to a list of dn parts
    if decompose=True return a list of tuple (one for each dn component) else return a list of strings
    if remove_space=True removes unneeded spaces
    if space_around_equal=True add spaces around equal in returned strings
    if separate_rdn=True consider multiple RDNs as different component of DN
    """

def parse_dn(dn, escape: bool = False, strip: bool = False):
    """
    Parses a DN into syntactic components
    :param dn:
    :param escape:
    :param strip:
    :return:
    a list of tripels representing `attributeTypeAndValue` elements
    containing `attributeType`, `attributeValue` and the following separator (`COMMA` or `PLUS`) if given, else an empty `str`.
    in their original representation, still containing escapes or encoded as hex.
    """

def safe_dn(dn, decompose: bool = False, reverse: bool = False):
    """
    normalize and escape a dn, if dn is a sequence it is joined.
    the reverse parameter changes the join direction of the sequence
    """

def safe_rdn(dn, decompose: bool = False):
    """Returns a list of rdn for the dn, usually there is only one rdn, but it can be more than one when the + sign is used"""

def escape_rdn(rdn: str) -> str:
    """
    Escape rdn characters to prevent injection according to RFC 4514.
    """
