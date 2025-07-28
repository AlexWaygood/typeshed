""" """

def check_backslash(value): ...
def check_type(input_value, value_type): ...
def always_valid(input_value): ...
def validate_generic_single_value(input_value): ...
def validate_zero_and_minus_one_and_positive_int(input_value):
    """Accept -1 and 0 only (used by pwdLastSet in AD)"""

def validate_integer(input_value): ...
def validate_bytes(input_value): ...
def validate_boolean(input_value): ...
def validate_time_with_0_year(input_value): ...
def validate_time(input_value): ...
def validate_ad_timestamp(input_value):
    """
    Active Directory stores date/time values as the number of 100-nanosecond intervals
    that have elapsed since the 0 hour on January 1, 1601 till the date/time that is being stored.
    The time is always stored in Greenwich Mean Time (GMT) in the Active Directory.
    """

def validate_ad_timedelta(input_value):
    """
    Should be validated like an AD timestamp except that since it is a time
    delta, it is stored as a negative number.
    """

def validate_guid(input_value):
    """
    object guid in uuid format (Novell eDirectory)
    """

def validate_uuid(input_value):
    """
    object entryUUID in uuid format
    """

def validate_uuid_le(input_value):
    """
    Active Directory stores objectGUID in uuid_le format, follows RFC4122 and MS-DTYP:
    "{07039e68-4373-264d-a0a7-07039e684373}": string representation big endian, converted to little endian (with or without brace curles)
    "689e030773434d26a7a007039e684373": packet representation, already in little endian
    "\\68\\9e\\03\\07\\73\\43\\4d\\26\\a7\\a0\\07\\03\\9e\\68\\43\\73": bytes representation, already in little endian
    byte sequence: already in little endian

    """

def validate_sid(input_value):
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

    If you have a SID like S-a-b-c-d-e-f-g-...

    Then the bytes are
    a       (revision)
    N       (number of dashes minus two)
    bbbbbb  (six bytes of "b" treated as a 48-bit number in big-endian format)
    cccc    (four bytes of "c" treated as a 32-bit number in little-endian format)
    dddd    (four bytes of "d" treated as a 32-bit number in little-endian format)
    eeee    (four bytes of "e" treated as a 32-bit number in little-endian format)
    ffff    (four bytes of "f" treated as a 32-bit number in little-endian format)

    """
