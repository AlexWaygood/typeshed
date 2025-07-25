""" """

from typing import Any

def constant_to_class_kind(value): ...
def constant_to_attribute_usage(value): ...
def attribute_usage_to_constant(value): ...
def quoted_string_to_list(quoted_string): ...
def oids_string_to_list(oid_string): ...
def extension_to_tuple(extension_string): ...
def list_to_string(list_object): ...

class BaseServerInfo:
    raw: Any
    def __init__(self, raw_attributes) -> None: ...
    @classmethod
    def from_json(cls, json_definition, schema=None, custom_formatter=None): ...
    @classmethod
    def from_file(cls, target, schema=None, custom_formatter=None): ...
    def to_file(self, target, indent: int = 4, sort: bool = True) -> None: ...
    def to_json(self, indent: int = 4, sort: bool = True): ...

class DsaInfo(BaseServerInfo):
    """
    This class contains info about the ldap server (DSA) read from DSE
    as defined in RFC4512 and RFC3045. Unknown attributes are stored in the "other" dict
    """

    alt_servers: Any
    naming_contexts: Any
    supported_controls: Any
    supported_extensions: Any
    supported_features: Any
    supported_ldap_versions: Any
    supported_sasl_mechanisms: Any
    vendor_name: Any
    vendor_version: Any
    schema_entry: Any
    other: Any
    def __init__(self, attributes, raw_attributes) -> None: ...

class SchemaInfo(BaseServerInfo):
    """
    This class contains info about the ldap server schema read from an entry (default entry is DSE)
    as defined in RFC4512. Unknown attributes are stored in the "other" dict
    """

    schema_entry: Any
    create_time_stamp: Any
    modify_time_stamp: Any
    attribute_types: Any
    object_classes: Any
    matching_rules: Any
    matching_rule_uses: Any
    dit_content_rules: Any
    dit_structure_rules: Any
    name_forms: Any
    ldap_syntaxes: Any
    other: Any
    def __init__(self, schema_entry, attributes, raw_attributes) -> None: ...
    def is_valid(self): ...

class BaseObjectInfo:
    """
    Base class for objects defined in the schema as per RFC4512
    """

    oid: Any
    name: Any
    description: Any
    obsolete: Any
    extensions: Any
    experimental: Any
    raw_definition: Any
    def __init__(
        self, oid=None, name=None, description=None, obsolete: bool = False, extensions=None, experimental=None, definition=None
    ) -> None: ...
    @property
    def oid_info(self): ...
    @classmethod
    def from_definition(cls, definitions): ...

class MatchingRuleInfo(BaseObjectInfo):
    """
    As per RFC 4512 (4.1.3)
    """

    syntax: Any
    def __init__(
        self,
        oid=None,
        name=None,
        description=None,
        obsolete: bool = False,
        syntax=None,
        extensions=None,
        experimental=None,
        definition=None,
    ) -> None: ...

class MatchingRuleUseInfo(BaseObjectInfo):
    """
    As per RFC 4512 (4.1.4)
    """

    apply_to: Any
    def __init__(
        self,
        oid=None,
        name=None,
        description=None,
        obsolete: bool = False,
        apply_to=None,
        extensions=None,
        experimental=None,
        definition=None,
    ) -> None: ...

class ObjectClassInfo(BaseObjectInfo):
    """
    As per RFC 4512 (4.1.1)
    """

    superior: Any
    kind: Any
    must_contain: Any
    may_contain: Any
    def __init__(
        self,
        oid=None,
        name=None,
        description=None,
        obsolete: bool = False,
        superior=None,
        kind=None,
        must_contain=None,
        may_contain=None,
        extensions=None,
        experimental=None,
        definition=None,
    ) -> None: ...

class AttributeTypeInfo(BaseObjectInfo):
    """
    As per RFC 4512 (4.1.2)
    """

    superior: Any
    equality: Any
    ordering: Any
    substring: Any
    syntax: Any
    min_length: Any
    single_value: Any
    collective: Any
    no_user_modification: Any
    usage: Any
    mandatory_in: Any
    optional_in: Any
    def __init__(
        self,
        oid=None,
        name=None,
        description=None,
        obsolete: bool = False,
        superior=None,
        equality=None,
        ordering=None,
        substring=None,
        syntax=None,
        min_length=None,
        single_value: bool = False,
        collective: bool = False,
        no_user_modification: bool = False,
        usage=None,
        extensions=None,
        experimental=None,
        definition=None,
    ) -> None: ...

class LdapSyntaxInfo(BaseObjectInfo):
    """
    As per RFC 4512 (4.1.5)
    """

    def __init__(self, oid=None, description=None, extensions=None, experimental=None, definition=None) -> None: ...

class DitContentRuleInfo(BaseObjectInfo):
    """
    As per RFC 4512 (4.1.6)
    """

    auxiliary_classes: Any
    must_contain: Any
    may_contain: Any
    not_contains: Any
    def __init__(
        self,
        oid=None,
        name=None,
        description=None,
        obsolete: bool = False,
        auxiliary_classes=None,
        must_contain=None,
        may_contain=None,
        not_contains=None,
        extensions=None,
        experimental=None,
        definition=None,
    ) -> None: ...

class DitStructureRuleInfo(BaseObjectInfo):
    """
    As per RFC 4512 (4.1.7.1)
    """

    superior: Any
    name_form: Any
    def __init__(
        self,
        oid=None,
        name=None,
        description=None,
        obsolete: bool = False,
        name_form=None,
        superior=None,
        extensions=None,
        experimental=None,
        definition=None,
    ) -> None: ...

class NameFormInfo(BaseObjectInfo):
    """
    As per RFC 4512 (4.1.7.2)
    """

    object_class: Any
    must_contain: Any
    may_contain: Any
    def __init__(
        self,
        oid=None,
        name=None,
        description=None,
        obsolete: bool = False,
        object_class=None,
        must_contain=None,
        may_contain=None,
        extensions=None,
        experimental=None,
        definition=None,
    ) -> None: ...
