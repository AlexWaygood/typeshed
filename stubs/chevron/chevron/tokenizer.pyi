from collections.abc import Iterator

class ChevronError(SyntaxError): ...

def grab_literal(template: str, l_del: str | None) -> tuple[str, str]:  # undocumented
    """Parse a literal from the template"""

def l_sa_check(template: str, literal: str, is_standalone: bool) -> bool | None:  # undocumented
    """Do a preliminary check to see if a tag could be a standalone"""

def r_sa_check(template: str, tag_type: str, is_standalone: bool) -> bool:  # undocumented
    """Do a final checkto see if a tag could be a standalone"""

def parse_tag(template: str, l_del: str | None, r_del: str | None) -> tuple[tuple[str, str], str]:  # undocumented
    """Parse a tag from a template"""

def tokenize(
    template: str, def_ldel: str | None = "{{", def_rdel: str | None = "}}"
) -> Iterator[tuple[str, str]]:  # undocumented
    """Tokenize a mustache template

    Tokenizes a mustache template in a generator fashion,
    using file-like objects. It also accepts a string containing
    the template.


    Arguments:

    template -- a file-like object, or a string of a mustache template

    def_ldel -- The default left delimiter
                ("{{" by default, as in spec compliant mustache)

    def_rdel -- The default right delimiter
                ("}}" by default, as in spec compliant mustache)


    Returns:

    A generator of mustache tags in the form of a tuple

    -- (tag_type, tag_key)

    Where tag_type is one of:
     * literal
     * section
     * inverted section
     * end
     * partial
     * no escape

    And tag_key is either the key or in the case of a literal tag,
    the literal itself.
    """
