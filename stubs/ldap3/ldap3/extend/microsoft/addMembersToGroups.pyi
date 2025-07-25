""" """

def ad_add_members_to_groups(connection, members_dn, groups_dn, fix: bool = True, raise_error: bool = False):
    """
    :param connection: a bound Connection object
    :param members_dn: the list of members to add to groups
    :param groups_dn: the list of groups where members are to be added
    :param fix: checks for group existence and already assigned members
    :param raise_error: If the operation fails it raises an error instead of returning False
    :return: a boolean where True means that the operation was successful and False means an error has happened
    Establishes users-groups relations following the Active Directory rules: users are added to the member attribute of groups.
    Raises LDAPInvalidDnError if members or groups are not found in the DIT.
    """
