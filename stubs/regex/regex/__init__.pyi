"""Support for regular expressions (RE).

This module provides regular expression matching operations similar to those
found in Perl. It supports both 8-bit and Unicode strings; both the pattern and
the strings being processed can contain null bytes and characters outside the
US ASCII range.

Regular expressions can contain both special and ordinary characters. Most
ordinary characters, like "A", "a", or "0", are the simplest regular
expressions; they simply match themselves. You can concatenate ordinary
characters, so last matches the string 'last'.

There are a few differences between the old (legacy) behaviour and the new
(enhanced) behaviour, which are indicated by VERSION0 or VERSION1.

The special characters are:
    "."                 Matches any character except a newline.
    "^"                 Matches the start of the string.
    "$"                 Matches the end of the string or just before the
                        newline at the end of the string.
    "*"                 Matches 0 or more (greedy) repetitions of the preceding
                        RE. Greedy means that it will match as many repetitions
                        as possible.
    "+"                 Matches 1 or more (greedy) repetitions of the preceding
                        RE.
    "?"                 Matches 0 or 1 (greedy) of the preceding RE.
    *?,+?,??            Non-greedy versions of the previous three special
                        characters.
    *+,++,?+            Possessive versions of the previous three special
                        characters.
    {m,n}               Matches from m to n repetitions of the preceding RE.
    {m,n}?              Non-greedy version of the above.
    {m,n}+              Possessive version of the above.
    {...}               Fuzzy matching constraints.
    "\\\\"                Either escapes special characters or signals a special
                        sequence.
    [...]               Indicates a set of characters. A "^" as the first
                        character indicates a complementing set.
    "|"                 A|B, creates an RE that will match either A or B.
    (...)               Matches the RE inside the parentheses. The contents are
                        captured and can be retrieved or matched later in the
                        string.
    (?flags-flags)      VERSION1: Sets/clears the flags for the remainder of
                        the group or pattern; VERSION0: Sets the flags for the
                        entire pattern.
    (?:...)             Non-capturing version of regular parentheses.
    (?>...)             Atomic non-capturing version of regular parentheses.
    (?flags-flags:...)  Non-capturing version of regular parentheses with local
                        flags.
    (?P<name>...)       The substring matched by the group is accessible by
                        name.
    (?<name>...)        The substring matched by the group is accessible by
                        name.
    (?P=name)           Matches the text matched earlier by the group named
                        name.
    (?#...)             A comment; ignored.
    (?=...)             Matches if ... matches next, but doesn't consume the
                        string.
    (?!...)             Matches if ... doesn't match next.
    (?<=...)            Matches if preceded by ....
    (?<!...)            Matches if not preceded by ....
    (?(id)yes|no)       Matches yes pattern if group id matched, the (optional)
                        no pattern otherwise.
    (?(DEFINE)...)      If there's no group called "DEFINE", then ... will be
                        ignored, but any group definitions will be available.
    (?|...|...)         (?|A|B), creates an RE that will match either A or B,
                        but reuses capture group numbers across the
                        alternatives.
    (*FAIL)             Forces matching to fail, which means immediate
                        backtracking.
    (*F)                Abbreviation for (*FAIL).
    (*PRUNE)            Discards the current backtracking information. Its
                        effect doesn't extend outside an atomic group or a
                        lookaround.
    (*SKIP)             Similar to (*PRUNE), except that it also sets where in
                        the text the next attempt at matching the entire
                        pattern will start. Its effect doesn't extend outside
                        an atomic group or a lookaround.

The fuzzy matching constraints are: "i" to permit insertions, "d" to permit
deletions, "s" to permit substitutions, "e" to permit any of these. Limits are
optional with "<=" and "<". If any type of error is provided then any type not
provided is not permitted.

A cost equation may be provided.

Examples:
    (?:fuzzy){i<=2}
    (?:fuzzy){i<=1,s<=2,d<=1,1i+1s+1d<3}

VERSION1: Set operators are supported, and a set can include nested sets. The
set operators, in order of increasing precedence, are:
    ||  Set union ("x||y" means "x or y").
    ~~  (double tilde) Symmetric set difference ("x~~y" means "x or y, but not
        both").
    &&  Set intersection ("x&&y" means "x and y").
    --  (double dash) Set difference ("x--y" means "x but not y").

Implicit union, ie, simple juxtaposition like in [ab], has the highest
precedence.

VERSION0 and VERSION1:
The special sequences consist of "\\\\" and a character from the list below. If
the ordinary character is not on the list, then the resulting RE will match the
second character.
    \\number         Matches the contents of the group of the same number if
                    number is no more than 2 digits, otherwise the character
                    with the 3-digit octal code.
    \\a              Matches the bell character.
    \\A              Matches only at the start of the string.
    \\b              Matches the empty string, but only at the start or end of a
                    word.
    \\B              Matches the empty string, but not at the start or end of a
                    word.
    \\d              Matches any decimal digit; equivalent to the set [0-9] when
                    matching a bytestring or a Unicode string with the ASCII
                    flag, or the whole range of Unicode digits when matching a
                    Unicode string.
    \\D              Matches any non-digit character; equivalent to [^\\d].
    \\f              Matches the formfeed character.
    \\g<name>        Matches the text matched by the group named name.
    \\G              Matches the empty string, but only at the position where
                    the search started.
    \\h              Matches horizontal whitespace.
    \\K              Keeps only what follows for the entire match.
    \\L<name>        Named list. The list is provided as a keyword argument.
    \\m              Matches the empty string, but only at the start of a word.
    \\M              Matches the empty string, but only at the end of a word.
    \\n              Matches the newline character.
    \\N{name}        Matches the named character.
    \\p{name=value}  Matches the character if its property has the specified
                    value.
    \\P{name=value}  Matches the character if its property hasn't the specified
                    value.
    \\r              Matches the carriage-return character.
    \\s              Matches any whitespace character; equivalent to
                    [ \\t\\n\\r\\f\\v].
    \\S              Matches any non-whitespace character; equivalent to [^\\s].
    \\t              Matches the tab character.
    \\uXXXX          Matches the Unicode codepoint with 4-digit hex code XXXX.
    \\UXXXXXXXX      Matches the Unicode codepoint with 8-digit hex code
                    XXXXXXXX.
    \\v              Matches the vertical tab character.
    \\w              Matches any alphanumeric character; equivalent to
                    [a-zA-Z0-9_] when matching a bytestring or a Unicode string
                    with the ASCII flag, or the whole range of Unicode
                    alphanumeric characters (letters plus digits plus
                    underscore) when matching a Unicode string. With LOCALE, it
                    will match the set [0-9_] plus characters defined as
                    letters for the current locale.
    \\W              Matches the complement of \\w; equivalent to [^\\w].
    \\xXX            Matches the character with 2-digit hex code XX.
    \\X              Matches a grapheme.
    \\Z              Matches only at the end of the string.
    \\\\              Matches a literal backslash.

This module exports the following functions:
    match      Match a regular expression pattern at the beginning of a string.
    fullmatch  Match a regular expression pattern against all of a string.
    search     Search a string for the presence of a pattern.
    sub        Substitute occurrences of a pattern found in a string using a
               template string.
    subf       Substitute occurrences of a pattern found in a string using a
               format string.
    subn       Same as sub, but also return the number of substitutions made.
    subfn      Same as subf, but also return the number of substitutions made.
    split      Split a string by the occurrences of a pattern. VERSION1: will
               split at zero-width match; VERSION0: won't split at zero-width
               match.
    splititer  Return an iterator yielding the parts of a split string.
    findall    Find all occurrences of a pattern in a string.
    finditer   Return an iterator yielding a match object for each match.
    compile    Compile a pattern into a Pattern object.
    purge      Clear the regular expression cache.
    escape     Backslash all non-alphanumerics or special characters in a
               string.

Most of the functions support a concurrent parameter: if True, the GIL will be
released during matching, allowing other Python threads to run concurrently. If
the string changes during matching, the behaviour is undefined. This parameter
is not needed when working on the builtin (immutable) string classes.

Some of the functions in this module take flags as optional parameters. Most of
these flags can also be set within an RE:
    A   a   ASCII         Make \\w, \\W, \\b, \\B, \\d, and \\D match the
                          corresponding ASCII character categories. Default
                          when matching a bytestring.
    B   b   BESTMATCH     Find the best fuzzy match (default is first).
    D       DEBUG         Print the parsed pattern.
    E   e   ENHANCEMATCH  Attempt to improve the fit after finding the first
                          fuzzy match.
    F   f   FULLCASE      Use full case-folding when performing
                          case-insensitive matching in Unicode.
    I   i   IGNORECASE    Perform case-insensitive matching.
    L   L   LOCALE        Make \\w, \\W, \\b, \\B, \\d, and \\D dependent on the
                          current locale. (One byte per character only.)
    M   m   MULTILINE     "^" matches the beginning of lines (after a newline)
                          as well as the string. "$" matches the end of lines
                          (before a newline) as well as the end of the string.
    P   p   POSIX         Perform POSIX-standard matching (leftmost longest).
    R   r   REVERSE       Searches backwards.
    S   s   DOTALL        "." matches any character at all, including the
                          newline.
    U   u   UNICODE       Make \\w, \\W, \\b, \\B, \\d, and \\D dependent on the
                          Unicode locale. Default when matching a Unicode
                          string.
    V0  V0  VERSION0      Turn on the old legacy behaviour.
    V1  V1  VERSION1      Turn on the new enhanced behaviour. This flag
                          includes the FULLCASE flag.
    W   w   WORD          Make \\b and \\B work with default Unicode word breaks
                          and make ".", "^" and "$" work with Unicode line
                          breaks.
    X   x   VERBOSE       Ignore whitespace and comments for nicer looking REs.

This module also defines an exception 'error'.

"""

from .regex import *
