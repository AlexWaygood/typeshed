""" """

from pyasn1.type.namedtype import NamedTypes
from pyasn1.type.tag import TagSet
from pyasn1.type.univ import OctetString, Sequence

class UserIdentity(OctetString):
    """
    userIdentity [0] OCTET STRING OPTIONAL
    """

    tagSet: TagSet
    encoding: str

class OldPasswd(OctetString):
    """
    oldPasswd [1] OCTET STRING OPTIONAL
    """

    tagSet: TagSet
    encoding: str

class NewPasswd(OctetString):
    """
    newPasswd [2] OCTET STRING OPTIONAL
    """

    tagSet: TagSet
    encoding: str

class GenPasswd(OctetString):
    """
    newPasswd [2] OCTET STRING OPTIONAL
    """

    tagSet: TagSet
    encoding: str

class PasswdModifyRequestValue(Sequence):
    """
    PasswdModifyRequestValue ::= SEQUENCE {
        userIdentity [0] OCTET STRING OPTIONAL
        oldPasswd [1] OCTET STRING OPTIONAL
        newPasswd [2] OCTET STRING OPTIONAL }
    """

    componentType: NamedTypes

class PasswdModifyResponseValue(Sequence):
    """
    PasswdModifyResponseValue ::= SEQUENCE {
       genPasswd [0] OCTET STRING OPTIONAL }
    """

    componentType: NamedTypes
