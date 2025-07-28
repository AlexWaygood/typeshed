""" """

def sasl_prep(data):
    """
    implement SASLPrep profile as per RFC4013:
    it defines the "SASLprep" profile of the "stringprep" algorithm [StringPrep].
    The profile is designed for use in Simple Authentication and Security
    Layer ([SASL]) mechanisms, such as [PLAIN], [CRAM-MD5], and
    [DIGEST-MD5].  It may be applicable where simple user names and
    passwords are used.  This profile is not intended for use in
    preparing identity strings that are not simple user names (e.g.,
    email addresses, domain names, distinguished names), or where
    identity or password strings that are not character data, or require
    different handling (e.g., case folding).
    """

def validate_simple_password(password, accept_empty: bool = False):
    """
    validate simple password as per RFC4013 using sasl_prep:
    """

def abort_sasl_negotiation(connection, controls): ...
def send_sasl_negotiation(connection, controls, payload): ...
def random_hex_string(size): ...
