"""passlib.handlers.postgres_md5 - MD5-based algorithm used by Postgres for pg_shadow table"""

from typing import ClassVar

import passlib.utils.handlers as uh

class postgres_md5(uh.HasUserContext, uh.StaticHandler):
    """This class implements the Postgres MD5 Password hash, and follows the :ref:`password-hash-api`.

    It does a single round of hashing, and relies on the username as the salt.

    The :meth:`~passlib.ifc.PasswordHash.hash`, :meth:`~passlib.ifc.PasswordHash.genhash`, and :meth:`~passlib.ifc.PasswordHash.verify` methods all require the
    following additional contextual keywords:

    :type user: str
    :param user: name of postgres user account this password is associated with.
    """

    name: ClassVar[str]
    checksum_chars: ClassVar[str]
    checksum_size: ClassVar[int]

__all__ = ["postgres_md5"]
