""" """

def ad_remove_members_from_groups(connection, members_dn, groups_dn, fix, raise_error: bool = False):
    """
    :param connection: a bound Connection object
    :param members_dn: the list of members to remove from groups
    :param groups_dn: the list of groups where members are to be removed
    :param fix: checks for group existence and existing members
    :param raise_error: If the operation fails it raises an error instead of returning False
    :return: a boolean where True means that the operation was successful and False means an error has happened
    Removes users-groups relations following the Activwe Directory rules: users are removed from groups' member attribute

    """
