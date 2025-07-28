"""passlib.crypto.des -- DES block encryption routines

History
=======
These routines (which have since been drastically modified for python)
are based on a Java implementation of the des-crypt algorithm,
found at `<http://www.dynamic.net.au/christos/crypt/UnixCrypt2.txt>`_.

The copyright & license for that source is as follows::

    UnixCrypt.java 0.9 96/11/25
    Copyright (c) 1996 Aki Yoshida. All rights reserved.
    Permission to use, copy, modify and distribute this software
    for non-commercial or commercial purposes and without fee is
    hereby granted provided that this copyright notice appears in
    all copies.

    ---

    Unix crypt(3C) utility
    @version 0.9, 11/25/96
    @author  Aki Yoshida

    ---

    modified April 2001
    by Iris Van den Broeke, Daniel Deville

    ---
    Unix Crypt.
    Implements the one way cryptography used by Unix systems for
    simple password protection.
    @version $Id: UnixCrypt2.txt,v 1.1.1.1 2005/09/13 22:20:13 christos Exp $
    @author Greg Wilkins (gregw)

The netbsd des-crypt implementation has some nice notes on how this all works -
    http://fxr.googlebit.com/source/lib/libcrypt/crypt.c?v=NETBSD-CURRENT
"""

__all__ = ["expand_des_key", "des_encrypt_block"]

def expand_des_key(key):
    """convert DES from 7 bytes to 8 bytes (by inserting empty parity bits)"""

def des_encrypt_block(key, input, salt: int = 0, rounds: int = 1):
    """encrypt single block of data using DES, operates on 8-byte strings.

    :arg key:
        DES key as 7 byte string, or 8 byte string with parity bits
        (parity bit values are ignored).

    :arg input:
        plaintext block to encrypt, as 8 byte string.

    :arg salt:
        Optional 24-bit integer used to mutate the base DES algorithm in a
        manner specific to :class:`~passlib.hash.des_crypt` and its variants.
        The default value ``0`` provides the normal (unsalted) DES behavior.
        The salt functions as follows:
        if the ``i``'th bit of ``salt`` is set,
        bits ``i`` and ``i+24`` are swapped in the DES E-box output.

    :arg rounds:
        Optional number of rounds of to apply the DES key schedule.
        the default (``rounds=1``) provides the normal DES behavior,
        but :class:`~passlib.hash.des_crypt` and its variants use
        alternate rounds values.

    :raises TypeError: if any of the provided args are of the wrong type.
    :raises ValueError:
        if any of the input blocks are the wrong size,
        or the salt/rounds values are out of range.

    :returns:
        resulting 8-byte ciphertext block.
    """

def des_encrypt_int_block(key, input, salt: int = 0, rounds: int = 1):
    """encrypt single block of data using DES, operates on 64-bit integers.

    this function is essentially the same as :func:`des_encrypt_block`,
    except that it operates on integers, and will NOT automatically
    expand 56-bit keys if provided (since there's no way to detect them).

    :arg key:
        DES key as 64-bit integer (the parity bits are ignored).

    :arg input:
        input block as 64-bit integer

    :arg salt:
        optional 24-bit integer used to mutate the base DES algorithm.
        defaults to ``0`` (no mutation applied).

    :arg rounds:
        optional number of rounds of to apply the DES key schedule.
        defaults to ``1``.

    :raises TypeError: if any of the provided args are of the wrong type.
    :raises ValueError:
        if any of the input blocks are the wrong size,
        or the salt/rounds values are out of range.

    :returns:
        resulting ciphertext as 64-bit integer.
    """
