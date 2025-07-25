"""passlib.handlers.mysql

MySQL 3.2.3 / OLD_PASSWORD()

    This implements Mysql's OLD_PASSWORD algorithm, introduced in version 3.2.3, deprecated in version 4.1.

    See :mod:`passlib.handlers.mysql_41` for the new algorithm was put in place in version 4.1

    This algorithm is known to be very insecure, and should only be used to verify existing password hashes.

    http://djangosnippets.org/snippets/1508/

MySQL 4.1.1 / NEW PASSWORD
    This implements Mysql new PASSWORD algorithm, introduced in version 4.1.

    This function is unsalted, and therefore not very secure against rainbow attacks.
    It should only be used when dealing with mysql passwords,
    for all other purposes, you should use a salted hash function.

    Description taken from http://dev.mysql.com/doc/refman/6.0/en/password-hashing.html
"""

from typing import ClassVar

import passlib.utils.handlers as uh

__all__ = ["mysql323"]

class mysql323(uh.StaticHandler):
    """This class implements the MySQL 3.2.3 password hash, and follows the :ref:`password-hash-api`.

    It has no salt and a single fixed round.

    The :meth:`~passlib.ifc.PasswordHash.hash` and :meth:`~passlib.ifc.PasswordHash.genconfig` methods accept no optional keywords.
    """

    name: ClassVar[str]
    checksum_size: ClassVar[int]
    checksum_chars: ClassVar[str]

class mysql41(uh.StaticHandler):
    """This class implements the MySQL 4.1 password hash, and follows the :ref:`password-hash-api`.

    It has no salt and a single fixed round.

    The :meth:`~passlib.ifc.PasswordHash.hash` and :meth:`~passlib.ifc.PasswordHash.genconfig` methods accept no optional keywords.
    """

    name: ClassVar[str]
    checksum_chars: ClassVar[str]
    checksum_size: ClassVar[int]
