"""Built-in functions, types, exceptions, and other objects.

This module provides direct access to all 'built-in'
identifiers of Python; for example, builtins.len is
the full name for the built-in function len().

This module is not normally accessed explicitly by most
applications, but can be useful in modules that provide
objects with the same name as a built-in value, but in
which the built-in of that name is also needed.
"""

# six explicitly re-exports builtins. Normally this is something we'd want to avoid.
# But this is specifically a compatibility package.
from builtins import *  # noqa: UP029
