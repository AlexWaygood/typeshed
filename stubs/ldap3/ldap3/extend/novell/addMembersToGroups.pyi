""" """

def edir_add_members_to_groups(connection, members_dn, groups_dn, fix, transaction):
    """
    :param connection: a bound Connection object
    :param members_dn: the list of members to add to groups
    :param groups_dn: the list of groups where members are to be added
    :param fix: checks for inconsistences in the users-groups relation and fixes them
    :param transaction: activates an LDAP transaction
    :return: a boolean where True means that the operation was successful and False means an error has happened
    Establishes users-groups relations following the eDirectory rules: groups are added to securityEquals and groupMembership
    attributes in the member object while members are added to member and equivalentToMe attributes in the group object.
    Raises LDAPInvalidDnError if members or groups are not found in the DIT.
    """
