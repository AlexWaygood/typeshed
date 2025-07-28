""" """

def edir_check_groups_memberships(connection, members_dn, groups_dn, fix, transaction):
    """
    :param connection: a bound Connection object
    :param members_dn: the list of members to check
    :param groups_dn: the list of groups to check
    :param fix: checks for inconsistences in the users-groups relation and fixes them
    :param transaction: activates an LDAP transaction when fixing
    :return: a boolean where True means that the operation was successful and False means an error has happened
    Checks and fixes users-groups relations following the eDirectory rules: groups are checked against 'groupMembership'
    attribute in the member object while members are checked against 'member' attribute in the group object.
    Raises LDAPInvalidDnError if members or groups are not found in the DIT.
    """
