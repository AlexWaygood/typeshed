""" """

def parse_uri(uri):
    """
    Decode LDAP URI as specified in RFC 4516 relaxing specifications
    permitting 'ldaps' as scheme for ssl-ldap
    """
