""" """

from typing import Any

def format_unicode(raw_value): ...
def format_integer(raw_value): ...
def format_binary(raw_value): ...
def format_uuid(raw_value): ...
def format_uuid_le(raw_value): ...
def format_boolean(raw_value): ...
def format_ad_timestamp(raw_value):
    """
    Active Directory stores date/time values as the number of 100-nanosecond intervals
    that have elapsed since the 0 hour on January 1, 1601 till the date/time that is being stored.
    The time is always stored in Greenwich Mean Time (GMT) in the Active Directory.
    """

time_format: Any

def format_time(raw_value): ...
def format_ad_timedelta(raw_value):
    """
    Convert a negative filetime value to a timedelta.
    """

def format_time_with_0_year(raw_value): ...
def format_sid(raw_value):
    """
    SID= "S-1-" IdentifierAuthority 1*SubAuthority
           IdentifierAuthority= IdentifierAuthorityDec / IdentifierAuthorityHex
              ; If the identifier authority is < 2^32, the
              ; identifier authority is represented as a decimal
              ; number
              ; If the identifier authority is >= 2^32,
              ; the identifier authority is represented in
              ; hexadecimal
            IdentifierAuthorityDec =  1*10DIGIT
              ; IdentifierAuthorityDec, top level authority of a
              ; security identifier is represented as a decimal number
            IdentifierAuthorityHex = "0x" 12HEXDIG
              ; IdentifierAuthorityHex, the top-level authority of a
              ; security identifier is represented as a hexadecimal number
            SubAuthority= "-" 1*10DIGIT
              ; Sub-Authority is always represented as a decimal number
              ; No leading "0" characters are allowed when IdentifierAuthority
              ; or SubAuthority is represented as a decimal number
              ; All hexadecimal digits must be output in string format,
              ; pre-pended by "0x"

    Revision (1 byte): An 8-bit unsigned integer that specifies the revision level of the SID. This value MUST be set to 0x01.
    SubAuthorityCount (1 byte): An 8-bit unsigned integer that specifies the number of elements in the SubAuthority array. The maximum number of elements allowed is 15.
    IdentifierAuthority (6 bytes): A SID_IDENTIFIER_AUTHORITY structure that indicates the authority under which the SID was created. It describes the entity that created the SID. The Identifier Authority value {0,0,0,0,0,5} denotes SIDs created by the NT SID authority.
    SubAuthority (variable): A variable length array of unsigned 32-bit integers that uniquely identifies a principal relative to the IdentifierAuthority. Its length is determined by SubAuthorityCount.
    """
