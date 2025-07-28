import os
from _typeshed import Incomplete
from typing import Final

from reportlab.pdfbase.pdfdoc import PDFObject
from reportlab.platypus.flowables import Flowable

__version__: Final[str]

def xorKey(num, key):
    """xor's each byte of the key with the number, which is <256"""

CLOBBERID: int
CLOBBERPERMISSIONS: int
DEBUG: Incomplete
reserved1: int
reserved2: Incomplete
printable: Incomplete
modifiable: Incomplete
copypastable: Incomplete
annotatable: Incomplete
higherbits: int

os_urandom = os.urandom

class StandardEncryption:
    prepared: int
    userPassword: Incomplete
    ownerPassword: Incomplete
    revision: int
    canPrint: Incomplete
    canModify: Incomplete
    canCopy: Incomplete
    canAnnotate: Incomplete
    O: Incomplete
    def __init__(
        self,
        userPassword,
        ownerPassword=None,
        canPrint: int = 1,
        canModify: int = 1,
        canCopy: int = 1,
        canAnnotate: int = 1,
        strength=None,
    ) -> None:
        """
        This class defines the encryption properties to be used while creating a pdf document.
        Once initiated, a StandardEncryption object can be applied to a Canvas or a BaseDocTemplate.
        The userPassword parameter sets the user password on the encrypted pdf.
        The ownerPassword parameter sets the owner password on the encrypted pdf.
        The boolean flags canPrint, canModify, canCopy, canAnnotate determine wether a user can
        perform the corresponding actions on the pdf when only a user password has been supplied.
        If the user supplies the owner password while opening the pdf, all actions can be performed regardless
        of the flags.
        Note that the security provided by these encryption settings (and even more so for the flags) is very weak.
        """

    def setAllPermissions(self, value) -> None: ...
    def permissionBits(self): ...
    def encode(self, t):
        """encode a string, stream, text"""
    P: Incomplete
    key: Incomplete
    U: Incomplete
    UE: Incomplete
    OE: Incomplete
    Perms: Incomplete
    objnum: Incomplete
    def prepare(self, document, overrideID=None) -> None: ...
    version: Incomplete
    def register(self, objnum, version) -> None: ...
    def info(self): ...

class StandardEncryptionDictionary(PDFObject):
    __RefOnly__: int
    revision: Incomplete
    def __init__(self, O, OE, U, UE, P, Perms, revision) -> None: ...
    def format(self, document): ...

padding: str

def hexText(text):
    """a legitimate way to show strings in PDF"""

def unHexText(hexText): ...

PadString: Incomplete

def checkRevision(revision): ...
def encryptionkey(password, OwnerKey, Permissions, FileId1, revision=None): ...
def computeO(userPassword, ownerPassword, revision): ...
def computeU(
    encryptionkey,
    encodestring=b"(\xbfN^Nu\x8aAd\x00NV\xff\xfa\x01\x08..\x00\xb6\xd0h>\x80/\x0c\xa9\xfedSiz",
    revision=None,
    documentId=None,
): ...
def checkU(encryptionkey, U) -> None: ...
def encodePDF(key, objectNumber, generationNumber, string, revision=None):
    """Encodes a string or stream"""

def equalityCheck(observed, expected, label) -> None: ...
def test() -> None: ...
def encryptCanvas(
    canvas,
    userPassword,
    ownerPassword=None,
    canPrint: int = 1,
    canModify: int = 1,
    canCopy: int = 1,
    canAnnotate: int = 1,
    strength: int = 40,
) -> None:
    """Applies encryption to the document being generated"""

class EncryptionFlowable(StandardEncryption, Flowable):
    """Drop this in your Platypus story and it will set up the encryption options.

    If you do it multiple times, the last one before saving will win.
    """

    def wrap(self, availWidth, availHeight): ...
    def draw(self) -> None: ...

def encryptDocTemplate(
    dt,
    userPassword,
    ownerPassword=None,
    canPrint: int = 1,
    canModify: int = 1,
    canCopy: int = 1,
    canAnnotate: int = 1,
    strength: int = 40,
) -> None:
    """For use in Platypus.  Call before build()."""

def encryptPdfInMemory(
    inputPDF,
    userPassword,
    ownerPassword=None,
    canPrint: int = 1,
    canModify: int = 1,
    canCopy: int = 1,
    canAnnotate: int = 1,
    strength: int = 40,
):
    """accepts a PDF file 'as a byte array in memory'; return encrypted one.

    This is a high level convenience and does not touch the hard disk in any way.
    If you are encrypting the same file over and over again, it's better to use
    pageCatcher and cache the results.
    """

def encryptPdfOnDisk(
    inputFileName,
    outputFileName,
    userPassword,
    ownerPassword=None,
    canPrint: int = 1,
    canModify: int = 1,
    canCopy: int = 1,
    canAnnotate: int = 1,
    strength: int = 40,
):
    """Creates encrypted file OUTPUTFILENAME.  Returns size in bytes."""

def scriptInterp() -> None: ...
def main() -> None: ...
