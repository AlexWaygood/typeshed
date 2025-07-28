"""
pygments.lexers.ldap
~~~~~~~~~~~~~~~~~~~~

Pygments lexers for LDAP.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from ..lexer import RegexLexer

__all__ = ["LdifLexer", "LdaprcLexer"]

class LdifLexer(RegexLexer):
    """
    Lexer for LDIF
    """

class LdaprcLexer(RegexLexer):
    """
    Lexer for OpenLDAP configuration files.
    """
