"""
olefile (formerly OleFileIO_PL)

Module to read/write Microsoft OLE2 files (also called Structured Storage or
Microsoft Compound Document File Format), such as Microsoft Office 97-2003
documents, Image Composer and FlashPix files, Outlook messages, ...
This version is compatible with Python 2.7 and 3.5+

Project website: https://www.decalage.info/olefile

olefile is copyright (c) 2005-2023 Philippe Lagadec
(https://www.decalage.info)

olefile is based on the OleFileIO module from the PIL library v1.1.7
See: http://www.pythonware.com/products/pil/index.htm
and http://svn.effbot.org/public/tags/pil-1.1.7/PIL/OleFileIO.py

The Python Imaging Library (PIL) is
Copyright (c) 1997-2009 by Secret Labs AB
Copyright (c) 1995-2009 by Fredrik Lundh

See source code and LICENSE.txt for information on usage and redistribution.
"""

import array
import datetime
import io
import logging
import traceback
from collections.abc import Sequence
from typing import IO, AnyStr, Generic
from typing_extensions import Self, TypeAlias

__date__: str
__version__: str
__author__: str

__all__ = [
    "isOleFile",
    "OleFileIO",
    "OleMetadata",
    "enable_logging",
    "MAGIC",
    "STGTY_EMPTY",
    "STGTY_STREAM",
    "STGTY_STORAGE",
    "STGTY_ROOT",
    "STGTY_PROPERTY",
    "STGTY_LOCKBYTES",
    "MINIMAL_OLEFILE_SIZE",
    "DEFECT_UNSURE",
    "DEFECT_POTENTIAL",
    "DEFECT_INCORRECT",
    "DEFECT_FATAL",
    "DEFAULT_PATH_ENCODING",
    "MAXREGSECT",
    "DIFSECT",
    "FATSECT",
    "ENDOFCHAIN",
    "FREESECT",
    "MAXREGSID",
    "NOSTREAM",
    "UNKNOWN_SIZE",
    "WORD_CLSID",
    "OleFileIONotClosed",
]

UINT32: str

DEFAULT_PATH_ENCODING: str | None

def get_logger(name: str, level: int = 51) -> logging.Logger:
    """
    Create a suitable logger object for this module.
    The goal is not to change settings of the root logger, to avoid getting
    other modules' logs on the screen.
    If a logger exists with same name, reuse it. (Else it would have duplicate
    handlers and messages would be doubled.)
    The level is set to CRITICAL+1 by default, to avoid any logging.
    """

log: logging.Logger

def enable_logging() -> None:
    """
    Enable logging for this module (disabled by default).
    This will set the module-specific logger level to NOTSET, which
    means the main application controls the actual logging level.
    """

MAGIC: bytes

MAXREGSECT: int
DIFSECT: int
FATSECT: int
ENDOFCHAIN: int
FREESECT: int

MAXREGSID: int
NOSTREAM: int

STGTY_EMPTY: int
STGTY_STORAGE: int
STGTY_STREAM: int
STGTY_LOCKBYTES: int
STGTY_PROPERTY: int
STGTY_ROOT: int

UNKNOWN_SIZE: int

VT_EMPTY: int
VT_NULL: int
VT_I2: int
VT_I4: int
VT_R4: int
VT_R8: int
VT_CY: int
VT_DATE: int
VT_BSTR: int
VT_DISPATCH: int
VT_ERROR: int
VT_BOOL: int
VT_VARIANT: int
VT_UNKNOWN: int
VT_DECIMAL: int
VT_I1: int
VT_UI1: int
VT_UI2: int
VT_UI4: int
VT_I8: int
VT_UI8: int
VT_INT: int
VT_UINT: int
VT_VOID: int
VT_HRESULT: int
VT_PTR: int
VT_SAFEARRAY: int
VT_CARRAY: int
VT_USERDEFINED: int
VT_LPSTR: int
VT_LPWSTR: int
VT_FILETIME: int
VT_BLOB: int
VT_STREAM: int
VT_STORAGE: int
VT_STREAMED_OBJECT: int
VT_STORED_OBJECT: int
VT_BLOB_OBJECT: int
VT_CF: int
VT_CLSID: int
VT_VECTOR: int

VT: dict[int, str]

WORD_CLSID: str
DEFECT_UNSURE: int
DEFECT_POTENTIAL: int
DEFECT_INCORRECT: int
DEFECT_FATAL: int
MINIMAL_OLEFILE_SIZE: int

def isOleFile(filename: IO[bytes] | bytes | str | None = None, data: bytes | None = None) -> bool:
    """
    Test if a file is an OLE container (according to the magic bytes in its header).

    .. note::
        This function only checks the first 8 bytes of the file, not the
        rest of the OLE structure.
        If data is provided, it also checks if the file size is above
        the minimal size of an OLE file (1536 bytes).
        If filename is provided with the path of the file on disk, the file is
        open only to read the first 8 bytes, then closed.

    .. versionadded:: 0.16

    :param filename: filename, contents or file-like object of the OLE file (string-like or file-like object)

        - if data is provided, filename is ignored.
        - if filename is a unicode string, it is used as path of the file to open on disk.
        - if filename is a bytes string smaller than 1536 bytes, it is used as path
          of the file to open on disk.
        - [deprecated] if filename is a bytes string longer than 1535 bytes, it is parsed
          as the content of an OLE file in memory. (bytes type only)
          Note that this use case is deprecated and should be replaced by the new data parameter
        - if filename is a file-like object (with read and seek methods),
          it is parsed as-is.
    :type filename: bytes, str, unicode or file-like object

    :param data: bytes string with the contents of the file to be checked, when the file is in memory
                 (added in olefile 0.47)
    :type data: bytes

    :returns: True if OLE, False otherwise.
    :rtype: bool
    """

def i8(c: bytes | int) -> int: ...
def i16(c: bytes, o: int = 0) -> int:
    """
    Converts a 2-bytes (16 bits) string to an integer.

    :param c: string containing bytes to convert
    :param o: offset of bytes to convert in string
    """

def i32(c: bytes, o: int = 0) -> int:
    """
    Converts a 4-bytes (32 bits) string to an integer.

    :param c: string containing bytes to convert
    :param o: offset of bytes to convert in string
    """

def _clsid(clsid: bytes) -> str:
    """
    Converts a CLSID to a human-readable string.

    :param clsid: string of length 16.
    """

def filetime2datetime(filetime: int) -> datetime.datetime:
    """
    convert FILETIME (64 bits int) to Python datetime.datetime
    """

class OleFileError(IOError):
    """
    Generic base error for this module.
    """

class NotOleFileError(OleFileError):
    """
    Error raised when the opened file is not an OLE file.
    """

class OleMetadata:
    """
    Class to parse and store metadata from standard properties of OLE files.

    Available attributes:
    codepage, title, subject, author, keywords, comments, template,
    last_saved_by, revision_number, total_edit_time, last_printed, create_time,
    last_saved_time, num_pages, num_words, num_chars, thumbnail,
    creating_application, security, codepage_doc, category, presentation_target,
    bytes, lines, paragraphs, slides, notes, hidden_slides, mm_clips,
    scale_crop, heading_pairs, titles_of_parts, manager, company, links_dirty,
    chars_with_spaces, unused, shared_doc, link_base, hlinks, hlinks_changed,
    version, dig_sig, content_type, content_status, language, doc_version

    Note: an attribute is set to None when not present in the properties of the
    OLE file.

    References for SummaryInformation stream:

    - https://msdn.microsoft.com/en-us/library/dd942545.aspx
    - https://msdn.microsoft.com/en-us/library/dd925819%28v=office.12%29.aspx
    - https://msdn.microsoft.com/en-us/library/windows/desktop/aa380376%28v=vs.85%29.aspx
    - https://msdn.microsoft.com/en-us/library/aa372045.aspx
    - http://sedna-soft.de/articles/summary-information-stream/
    - https://poi.apache.org/apidocs/org/apache/poi/hpsf/SummaryInformation.html

    References for DocumentSummaryInformation stream:

    - https://msdn.microsoft.com/en-us/library/dd945671%28v=office.12%29.aspx
    - https://msdn.microsoft.com/en-us/library/windows/desktop/aa380374%28v=vs.85%29.aspx
    - https://poi.apache.org/apidocs/org/apache/poi/hpsf/DocumentSummaryInformation.html

    New in version 0.25
    """

    SUMMARY_ATTRIBS: list[str]
    DOCSUM_ATTRIBS: list[str]

    def __init__(self) -> None:
        """
        Constructor for OleMetadata
        All attributes are set to None by default
        """

    def parse_properties(self, ole_file: OleFileIO[AnyStr]) -> None:
        """
        Parse standard properties of an OLE file, from the streams
        ``\\x05SummaryInformation`` and ``\\x05DocumentSummaryInformation``,
        if present.
        Properties are converted to strings, integers or python datetime objects.
        If a property is not present, its value is set to None.

        :param ole_file: OleFileIO object from which to parse properties
        """

    def dump(self) -> None:
        """
        Dump all metadata, for debugging purposes.
        """

class OleFileIONotClosed(RuntimeWarning):
    """
    Warning type used when OleFileIO is destructed but has open file handle.
    """

    def __init__(self, stack_of_open: traceback.FrameSummary | None = None) -> None: ...

class OleStream(io.BytesIO):
    """
    OLE2 Stream

    Returns a read-only file object which can be used to read
    the contents of a OLE stream (instance of the BytesIO class).
    To open a stream, use the openstream method in the OleFileIO class.

    This function can be used with either ordinary streams,
    or ministreams, depending on the offset, sectorsize, and
    fat table arguments.

    Attributes:

        - size: actual size of data stream, after it was opened.
    """

    def __init__(
        self,
        fp: IO[bytes],
        sect: int,
        size: int,
        offset: int,
        sectorsize: int,
        fat: list[int],
        filesize: int,
        olefileio: OleFileIO[AnyStr],
    ) -> None:
        """
        Constructor for OleStream class.

        :param fp: file object, the OLE container or the MiniFAT stream
        :param sect: sector index of first sector in the stream
        :param size: total size of the stream
        :param offset: offset in bytes for the first FAT or MiniFAT sector
        :param sectorsize: size of one sector
        :param fat: array/list of sector indexes (FAT or MiniFAT)
        :param filesize: size of OLE file (for debugging)
        :param olefileio: OleFileIO object containing this stream
        :returns: a BytesIO instance containing the OLE stream
        """

class OleDirectoryEntry(Generic[AnyStr]):
    """
    OLE2 Directory Entry pointing to a stream or a storage
    """

    STRUCT_DIRENTRY: str
    DIRENTRY_SIZE: int
    clsid: str

    def __init__(self, entry: bytes, sid: int, ole_file: OleFileIO[AnyStr]) -> None:
        """
        Constructor for an OleDirectoryEntry object.
        Parses a 128-bytes entry from the OLE Directory stream.

        :param bytes entry: bytes string (must be 128 bytes long)
        :param int sid: index of this directory entry in the OLE file directory
        :param OleFileIO ole_file: OleFileIO object containing this directory entry
        """

    def build_sect_chain(self, ole_file: OleFileIO[AnyStr]) -> None:
        """
        Build the sector chain for a stream (from the FAT or the MiniFAT)

        :param OleFileIO ole_file: OleFileIO object containing this directory entry
        :return: nothing
        """

    def build_storage_tree(self) -> None:
        """
        Read and build the red-black tree attached to this OleDirectoryEntry
        object, if it is a storage.
        Note that this method builds a tree of all subentries, so it should
        only be called for the root object once.
        """

    def append_kids(self, child_sid: int) -> None:
        """
        Walk through red-black tree of children of this directory entry to add
        all of them to the kids list. (recursive method)

        :param child_sid: index of child directory entry to use, or None when called
            first time for the root. (only used during recursion)
        """

    def __eq__(self, other: OleDirectoryEntry[AnyStr]) -> bool:  # type: ignore[override]
        """Compare entries by name"""

    def __lt__(self, other: OleDirectoryEntry[AnyStr]) -> bool:
        """Compare entries by name"""

    def __ne__(self, other: OleDirectoryEntry[AnyStr]) -> bool: ...  # type: ignore[override]
    def __le__(self, other: OleDirectoryEntry[AnyStr]) -> bool: ...
    def dump(self, tab: int = 0) -> None:
        """Dump this entry, and all its subentries (for debug purposes only)"""

    def getmtime(self) -> datetime.datetime | None:
        """
        Return modification time of a directory entry.

        :returns: None if modification time is null, a python datetime object
            otherwise (UTC timezone)

        new in version 0.26
        """

    def getctime(self) -> datetime.datetime | None:
        """
        Return creation time of a directory entry.

        :returns: None if modification time is null, a python datetime object
            otherwise (UTC timezone)

        new in version 0.26
        """

_Property: TypeAlias = int | str | bytes | bool | None

class OleFileIO(Generic[AnyStr]):
    """
    OLE container object

    This class encapsulates the interface to an OLE 2 structured
    storage file.  Use the listdir and openstream methods to
    access the contents of this file.

    Object names are given as a list of strings, one for each subentry
    level.  The root entry should be omitted.  For example, the following
    code extracts all image streams from a Microsoft Image Composer file::

        with OleFileIO("fan.mic") as ole:

            for entry in ole.listdir():
                if entry[1:2] == "Image":
                    fin = ole.openstream(entry)
                    fout = open(entry[0:1], "wb")
                    while True:
                        s = fin.read(8192)
                        if not s:
                            break
                        fout.write(s)

    You can use the viewer application provided with the Python Imaging
    Library to view the resulting files (which happens to be standard
    TIFF files).
    """

    root: OleDirectoryEntry[AnyStr] | None

    def __init__(
        self,
        filename: IO[bytes] | AnyStr | None = None,
        raise_defects: int = 40,
        write_mode: bool = False,
        debug: bool = False,
        path_encoding: str | None = DEFAULT_PATH_ENCODING,  # noqa: Y011
    ) -> None:
        """
        Constructor for the OleFileIO class.

        :param filename: file to open.

            - if filename is a string smaller than 1536 bytes, it is the path
              of the file to open. (bytes or unicode string)
            - if filename is a string longer than 1535 bytes, it is parsed
              as the content of an OLE file in memory. (bytes type only)
            - if filename is a file-like object (with read, seek and tell methods),
              it is parsed as-is. The caller is responsible for closing it when done.

        :param raise_defects: minimal level for defects to be raised as exceptions.
            (use DEFECT_FATAL for a typical application, DEFECT_INCORRECT for a
            security-oriented application, see source code for details)

        :param write_mode: bool, if True the file is opened in read/write mode instead
            of read-only by default.

        :param debug: bool, set debug mode (deprecated, not used anymore)

        :param path_encoding: None or str, name of the codec to use for path
            names (streams and storages), or None for Unicode.
            Unicode by default on Python 3+, UTF-8 on Python 2.x.
            (new in olefile 0.42, was hardcoded to Latin-1 until olefile v0.41)
        """

    def __del__(self) -> None:
        """Destructor, ensures all file handles are closed that we opened."""

    def __enter__(self) -> Self: ...
    def __exit__(self, *args: object) -> None: ...
    def _raise_defect(
        self, defect_level: int, message: str, exception_type: type[Exception] = OleFileError  # noqa: Y011
    ) -> None:
        """
        This method should be called for any defect found during file parsing.
        It may raise an OleFileError exception according to the minimal level chosen
        for the OleFileIO object.

        :param defect_level: defect level, possible values are:

            - DEFECT_UNSURE    : a case which looks weird, but not sure it's a defect
            - DEFECT_POTENTIAL : a potential defect
            - DEFECT_INCORRECT : an error according to specifications, but parsing can go on
            - DEFECT_FATAL     : an error which cannot be ignored, parsing is impossible

        :param message: string describing the defect, used with raised exception.
        :param exception_type: exception class to be raised, OleFileError by default
        """

    def _decode_utf16_str(self, utf16_str: bytes, errors: str = "replace") -> str | bytes:
        """
        Decode a string encoded in UTF-16 LE format, as found in the OLE
        directory or in property streams. Return a string encoded
        according to the path_encoding specified for the OleFileIO object.

        :param bytes utf16_str: bytes string encoded in UTF-16 LE format
        :param str errors: str, see python documentation for str.decode()
        :return: str, encoded according to path_encoding
        :rtype: str
        """

    def open(self, filename: IO[bytes] | AnyStr, write_mode: bool = False) -> None:
        """
        Open an OLE2 file in read-only or read/write mode.
        Read and parse the header, FAT and directory.

        :param filename: string-like or file-like object, OLE file to parse

            - if filename is a string smaller than 1536 bytes, it is the path
              of the file to open. (bytes or unicode string)
            - if filename is a string longer than 1535 bytes, it is parsed
              as the content of an OLE file in memory. (bytes type only)
            - if filename is a file-like object (with read, seek and tell methods),
              it is parsed as-is. The caller is responsible for closing it when done

        :param write_mode: bool, if True the file is opened in read/write mode instead
            of read-only by default. (ignored if filename is not a path)
        """

    def close(self) -> None:
        """
        close the OLE file, release the file object if we created it ourselves.

        Leaves the file handle open if it was provided by the caller.
        """

    def _close(self, warn: bool = False) -> None:
        """Implementation of close() with internal arg `warn`."""

    def _check_duplicate_stream(self, first_sect: int, minifat: bool = False) -> None:
        """
        Checks if a stream has not been already referenced elsewhere.
        This method should only be called once for each known stream, and only
        if stream size is not null.

        :param first_sect: int, index of first sector of the stream in FAT
        :param minifat: bool, if True, stream is located in the MiniFAT, else in the FAT
        """

    def dumpfat(self, fat: Sequence[int], firstindex: int = 0) -> None:
        """
        Display a part of FAT in human-readable form for debugging purposes
        """

    def dumpsect(self, sector: bytes, firstindex: int = 0) -> None:
        """
        Display a sector in a human-readable form, for debugging purposes
        """

    def sect2array(self, sect: bytes) -> Sequence[int]:
        """
        convert a sector to an array of 32 bits unsigned integers,
        swapping bytes on big endian CPUs such as PowerPC (old Macs)
        """

    def loadfat_sect(self, sect: bytes | array.array[int]) -> int | None:
        """
        Adds the indexes of the given sector to the FAT

        :param sect: string containing the first FAT sector, or array of long integers
        :returns: index of last FAT sector.
        """

    def loadfat(self, header: bytes) -> None:
        """
        Load the FAT table.
        """

    def loadminifat(self) -> None:
        """
        Load the MiniFAT table.
        """

    def getsect(self, sect: int) -> bytes:
        """
        Read given sector from file on disk.

        :param sect: int, sector index
        :returns: a string containing the sector data.
        """

    def write_sect(self, sect: int, data: bytes, padding: bytes = b"\x00") -> None:
        """
        Write given sector to file on disk.

        :param sect: int, sector index
        :param data: bytes, sector data
        :param padding: single byte, padding character if data < sector size
        """

    def _write_mini_sect(self, fp_pos: int, data: bytes, padding: bytes = b"\x00") -> None:
        """
        Write given sector to file on disk.

        :param fp_pos: int, file position
        :param data: bytes, sector data
        :param padding: single byte, padding character if data < sector size
        """

    def loaddirectory(self, sect: int) -> None:
        """
        Load the directory.

        :param sect: sector index of directory stream.
        """

    def _load_direntry(self, sid: int) -> OleDirectoryEntry[AnyStr]:
        """
        Load a directory entry from the directory.
        This method should only be called once for each storage/stream when
        loading the directory.

        :param sid: index of storage/stream in the directory.
        :returns: a OleDirectoryEntry object

        :exception OleFileError: if the entry has always been referenced.
        """

    def dumpdirectory(self) -> None:
        """
        Dump directory (for debugging only)
        """

    def _open(self, start: int, size: int = 0x7FFFFFFF, force_FAT: bool = False) -> OleStream:
        """
        Open a stream, either in FAT or MiniFAT according to its size.
        (openstream helper)

        :param start: index of first sector
        :param size: size of stream (or nothing if size is unknown)
        :param force_FAT: if False (default), stream will be opened in FAT or MiniFAT
            according to size. If True, it will always be opened in FAT.
        """

    def _list(
        self,
        files: list[list[AnyStr]],
        prefix: list[AnyStr],
        node: OleDirectoryEntry[AnyStr],
        streams: bool = True,
        storages: bool = False,
    ) -> None:
        """
        listdir helper

        :param files: list of files to fill in
        :param prefix: current location in storage tree (list of names)
        :param node: current node (OleDirectoryEntry object)
        :param streams: bool, include streams if True (True by default) - new in v0.26
        :param storages: bool, include storages if True (False by default) - new in v0.26
            (note: the root storage is never included)
        """

    def listdir(self, streams: bool = True, storages: bool = False) -> list[list[AnyStr]]:
        """
        Return a list of streams and/or storages stored in this file

        :param streams: bool, include streams if True (True by default) - new in v0.26
        :param storages: bool, include storages if True (False by default) - new in v0.26
            (note: the root storage is never included)
        :returns: list of stream and/or storage paths
        """

    def _find(self, filename: str | Sequence[str]) -> int:
        """
        Returns directory entry of given filename. (openstream helper)
        Note: this method is case-insensitive.

        :param filename: path of stream in storage tree (except root entry), either:

            - a string using Unix path syntax, for example:
              'storage_1/storage_1.2/stream'
            - or a list of storage filenames, path to the desired stream/storage.
              Example: ['storage_1', 'storage_1.2', 'stream']

        :returns: sid of requested filename
        :exception IOError: if file not found
        """

    def openstream(self, filename: AnyStr | Sequence[AnyStr]) -> OleStream:
        """
        Open a stream as a read-only file object (BytesIO).
        Note: filename is case-insensitive.

        :param filename: path of stream in storage tree (except root entry), either:

            - a string using Unix path syntax, for example:
              'storage_1/storage_1.2/stream'
            - or a list of storage filenames, path to the desired stream/storage.
              Example: ['storage_1', 'storage_1.2', 'stream']

        :returns: file object (read-only)
        :exception IOError: if filename not found, or if this is not a stream.
        """

    def _write_mini_stream(self, entry: OleDirectoryEntry[AnyStr], data_to_write: bytes) -> None: ...
    def write_stream(self, stream_name: str | Sequence[str], data: bytes) -> None:
        """
        Write a stream to disk. For now, it is only possible to replace an
        existing stream by data of the same size.

        :param stream_name: path of stream in storage tree (except root entry), either:

            - a string using Unix path syntax, for example:
              'storage_1/storage_1.2/stream'
            - or a list of storage filenames, path to the desired stream/storage.
              Example: ['storage_1', 'storage_1.2', 'stream']

        :param data: bytes, data to be written, must be the same size as the original
            stream.
        """

    def get_type(self, filename: AnyStr | Sequence[AnyStr]) -> bool | int:
        """
        Test if given filename exists as a stream or a storage in the OLE
        container, and return its type.

        :param filename: path of stream in storage tree. (see openstream for syntax)
        :returns: False if object does not exist, its entry type (>0) otherwise:

            - STGTY_STREAM: a stream
            - STGTY_STORAGE: a storage
            - STGTY_ROOT: the root entry
        """

    def getclsid(self, filename: AnyStr | Sequence[AnyStr]) -> str:
        """
        Return clsid of a stream/storage.

        :param filename: path of stream/storage in storage tree. (see openstream for
            syntax)
        :returns: Empty string if clsid is null, a printable representation of the clsid otherwise

        new in version 0.44
        """

    def getmtime(self, filename: AnyStr | Sequence[AnyStr]) -> datetime.datetime | None:
        """
        Return modification time of a stream/storage.

        :param filename: path of stream/storage in storage tree. (see openstream for
            syntax)
        :returns: None if modification time is null, a python datetime object
            otherwise (UTC timezone)

        new in version 0.26
        """

    def getctime(self, filename: AnyStr | Sequence[AnyStr]) -> datetime.datetime | None:
        """
        Return creation time of a stream/storage.

        :param filename: path of stream/storage in storage tree. (see openstream for
            syntax)
        :returns: None if creation time is null, a python datetime object
            otherwise (UTC timezone)

        new in version 0.26
        """

    def exists(self, filename: AnyStr | Sequence[AnyStr]) -> bool:
        """
        Test if given filename exists as a stream or a storage in the OLE
        container.
        Note: filename is case-insensitive.

        :param filename: path of stream in storage tree. (see openstream for syntax)
        :returns: True if object exist, else False.
        """

    def get_size(self, filename: AnyStr | Sequence[AnyStr]) -> int:
        """
        Return size of a stream in the OLE container, in bytes.

        :param filename: path of stream in storage tree (see openstream for syntax)
        :returns: size in bytes (long integer)
        :exception IOError: if file not found
        :exception TypeError: if this is not a stream.
        """

    def get_rootentry_name(self) -> bytes:
        """
        Return root entry name. Should usually be 'Root Entry' or 'R' in most
        implementations.
        """

    def getproperties(
        self, filename: AnyStr | Sequence[AnyStr], convert_time: bool = False, no_conversion: list[int] | None = None
    ) -> dict[int, list[_Property] | _Property]:
        """
        Return properties described in substream.

        :param filename: path of stream in storage tree (see openstream for syntax)
        :param convert_time: bool, if True timestamps will be converted to Python datetime
        :param no_conversion: None or list of int, timestamps not to be converted
            (for example total editing time is not a real timestamp)

        :returns: a dictionary of values indexed by id (integer)
        """

    def _parse_property(
        self, s: bytes, offset: int, property_id: int, property_type: int, convert_time: bool, no_conversion: list[int]
    ) -> list[_Property] | _Property: ...
    def _parse_property_basic(
        self, s: bytes, offset: int, property_id: int, property_type: int, convert_time: bool, no_conversion: list[int]
    ) -> tuple[_Property, int]: ...
    def get_metadata(self) -> OleMetadata:
        """
        Parse standard properties streams, return an OleMetadata object
        containing all the available metadata.
        (also stored in the metadata attribute of the OleFileIO object)

        new in version 0.25
        """

    def get_userdefined_properties(
        self, filename: AnyStr | Sequence[AnyStr], convert_time: bool = False, no_conversion: list[int] | None = None
    ) -> list[dict[str, bytes | int | None]]:
        """
        Return properties described in substream.

        :param filename: path of stream in storage tree (see openstream for syntax)
        :param convert_time: bool, if True timestamps will be converted to Python datetime
        :param no_conversion: None or list of int, timestamps not to be converted
            (for example total editing time is not a real timestamp)

        :returns: a dictionary of values indexed by id (integer)
        """

def main() -> None:
    """
    Main function when olefile is runs as a script from the command line.
    This will open an OLE2 file and display its structure and properties
    :return: nothing
    """
