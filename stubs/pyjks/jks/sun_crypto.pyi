from typing import Final

SUN_JKS_ALGO_ID: Final[tuple[int, ...]]
SUN_JCE_ALGO_ID: Final[tuple[int, ...]]

def jks_pkey_encrypt(key: bytes | bytearray, password_str: str) -> bytes:
    """
    Encrypts the private key with password protection algorithm used by JKS keystores.
    """

def jks_pkey_decrypt(data: bytes | bytearray, password_str: str) -> bytes:
    """
    Decrypts the private key password protection algorithm used by JKS keystores.
    The JDK sources state that 'the password is expected to be in printable ASCII', though this does not appear to be enforced;
    the password is converted into bytes simply by taking each individual Java char and appending its raw 2-byte representation.
    See sun/security/provider/KeyProtector.java in the JDK sources.
    """

def jce_pbe_decrypt(data: bytes | bytearray, password: str, salt: bytes, iteration_count: int) -> bytes:
    """
    Decrypts Sun's custom PBEWithMD5AndTripleDES password-based encryption scheme.
    It is based on password-based encryption as defined by the PKCS #5 standard, except that it uses triple DES instead of DES.
    Here's how this algorithm works:
      1. Create random salt and split it in two halves. If the two halves are identical, invert(*) the first half.
      2. Concatenate password with each of the halves.
      3. Digest each concatenation with c iterations, where c is the iterationCount. Concatenate the output from each digest round with the password,
         and use the result as the input to the next digest operation. The digest algorithm is MD5.
      4. After c iterations, use the 2 resulting digests as follows: The 16 bytes of the first digest and the 1st 8 bytes of the 2nd digest
         form the triple DES key, and the last 8 bytes of the 2nd digest form the IV.

    (*) Not actually an inversion operation due to an implementation bug in com.sun.crypto.provider.PBECipherCore. See _jce_invert_salt_half for details.
    See http://grepcode.com/file/repository.grepcode.com/java/root/jdk/openjdk/6-b27/com/sun/crypto/provider/PBECipherCore.java#PBECipherCore.deriveCipherKey%28java.security.Key%29
    """
