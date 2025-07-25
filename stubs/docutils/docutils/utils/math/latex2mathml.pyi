"""Convert LaTex maths code into presentational MathML.

This module is provisional:
the API is not settled and may change with any minor Docutils version.
"""

from collections.abc import Iterable

from docutils.utils.math.mathml_elements import MathElement, mover, msub, msubsup, msup, mtd, munder, munderover

letters: dict[str, str]
ordinary: dict[str, str]
greek_capitals: dict[str, str]
functions: dict[str, str | None]
modulo_functions: dict[str, tuple[bool, bool, bool, str]]
math_alphabets: dict[str, str]
stretchables: dict[str, str]
operators: dict[str, str]
thick_operators: dict[str, str]
small_operators: dict[str, str]
movablelimits: tuple[str, ...]
spaces: dict[str, str]
accents: dict[str, str]
over: dict[str, tuple[str, float]]
under: dict[str, tuple[str, float]]
anomalous_chars: dict[str, str]
mathbb: dict[str, str]
matrices: dict[str, tuple[str, str]]
layout_styles: dict[str, dict[str, bool | int]]
fractions: dict[str, dict[str, bool | int | str] | dict[str, bool | int] | dict[str, int]]
delimiter_sizes: list[str]
bigdelimiters: dict[str, int]

def tex_cmdname(string: str) -> tuple[str, str]:
    """Return leading TeX command name and remainder of `string`.

    >>> tex_cmdname('mymacro2') # up to first non-letter
    ('mymacro', '2')
    >>> tex_cmdname('name 2') # strip trailing whitespace
    ('name', '2')
    >>> tex_cmdname('_2') # single non-letter character
    ('_', '2')

    """

def tex_number(string: str) -> tuple[str, str]:
    """Return leading number literal and remainder of `string`.

    >>> tex_number('123.4')
    ('123.4', '')

    """

def tex_token(string: str) -> tuple[str, str]:
    """Return first simple TeX token and remainder of `string`.

    >>> tex_token('\\command{without argument}')
    ('\\command', '{without argument}')
    >>> tex_token('or first character')
    ('o', 'r first character')

    """

def tex_group(string: str) -> tuple[str, str]:
    """Return first TeX group or token and remainder of `string`.

    >>> tex_group('{first group} returned without brackets')
    ('first group', ' returned without brackets')

    """

def tex_token_or_group(string: str) -> tuple[str, str]:
    """Return first TeX group or token and remainder of `string`.

    >>> tex_token_or_group('\\command{without argument}')
    ('\\command', '{without argument}')
    >>> tex_token_or_group('first character')
    ('f', 'irst character')
    >>> tex_token_or_group(' also whitespace')
    (' ', 'also whitespace')
    >>> tex_token_or_group('{first group} keep rest')
    ('first group', ' keep rest')

    """

def tex_optarg(string: str) -> tuple[str, str]:
    """Return optional argument and remainder.

    >>> tex_optarg('[optional argument] returned without brackets')
    ('optional argument', ' returned without brackets')
    >>> tex_optarg('{empty string, if there is no optional arg}')
    ('', '{empty string, if there is no optional arg}')

    """

def parse_latex_math(root: MathElement, source: str) -> MathElement:
    """Append MathML conversion of `string` to `node` and return it.

    >>> parse_latex_math(math(), r'\x07lpha')
    math(mi('α'))
    >>> parse_latex_math(mrow(), r'x_{n}')
    mrow(msub(mi('x'), mi('n')))

    """

def handle_cmd(name: str, node: MathElement, string: str) -> tuple[MathElement, str]:
    """Process LaTeX command `name` followed by `string`.

    Append result to `node`.
    If needed, parse `string` for command argument.
    Return new current node and remainder of `string`:

    >>> handle_cmd('hbar', math(), r'
    rac')
    (math(mi('ℏ')), ' \\frac')
    >>> handle_cmd('hspace', math(), r'{1ex} (x)')
    (math(mspace(width='1ex')), ' (x)')

    """

def handle_math_alphabet(name: str, node: MathElement, string: str) -> tuple[MathElement, str]: ...
def handle_script_or_limit(node: MathElement, c: str, limits: str = "") -> munderover | msubsup | munder | msub | mover | msup:
    """Append script or limit element to `node`."""

def begin_environment(node: MathElement, string: str) -> tuple[mtd, str]: ...
def end_environment(node: MathElement, string: str) -> tuple[MathElement, str]: ...
def tex_equation_columns(rows: Iterable[str]) -> int: ...
def align_attributes(rows: Iterable[str]) -> dict[str, str | bool]: ...
def tex2mathml(tex_math: str, as_block: bool = False) -> str:
    """Return string with MathML code corresponding to `tex_math`.

    Set `as_block` to ``True`` for displayed formulas.
    """
