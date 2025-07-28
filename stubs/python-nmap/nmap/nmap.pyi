"""
nmap.py - version and date, see below

Source code : https://bitbucket.org/xael/python-nmap

Author :

* Alexandre Norman - norman at xael.org

Contributors:

* Steve 'Ashcrow' Milner - steve at gnulinux.net
* Brian Bustin - brian at bustin.us
* old.schepperhand
* Johan Lundberg
* Thomas D. maaaaz
* Robert Bost
* David Peltier
* Ed Jones

Licence: GPL v3 or any later version for python-nmap


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


**************
IMPORTANT NOTE
**************

The Nmap Security Scanner used by python-nmap is distributed
under it's own licence that you can find at https://svn.nmap.org/nmap/COPYING

Any redistribution of python-nmap along with the Nmap Security Scanner
must conform to the Nmap Security Scanner licence

"""

from collections.abc import Callable, Iterable, Iterator
from typing import Any, TypedDict, TypeVar
from typing_extensions import TypeAlias

_T = TypeVar("_T")
_Callback: TypeAlias = Callable[[str, _Result], object]

class _Result(TypedDict):
    nmap: _ResultNmap
    scan: dict[str, PortScannerHostDict]

class _ResultNmap(TypedDict):
    command_line: str
    scaninfo: _ResultNmapInfo
    scanstats: _ResultNampStats

class _ResultNmapInfo(TypedDict, total=False):
    error: str
    warning: str
    protocol: _ResultNampInfoProtocol

class _ResultNampInfoProtocol(TypedDict):
    method: str
    services: str

class _ResultNampStats(TypedDict):
    timestr: str
    elapsed: str
    uphosts: str
    downhosts: str
    totalhosts: str

class _ResulHostUptime(TypedDict):
    seconds: str
    lastboot: str

class _ResultHostNames(TypedDict):
    type: str
    name: str

class _ResultHostPort(TypedDict):
    conf: str
    cpe: str
    extrainfo: str
    name: str
    product: str
    reason: str
    state: str
    version: str

__last_modification__: str
__author__: str
__version__: str

class PortScanner:
    """
    PortScanner class allows to use nmap from python

    """

    def __init__(
        self,
        nmap_search_path: Iterable[str] = ("nmap", "/usr/bin/nmap", "/usr/local/bin/nmap", "/sw/bin/nmap", "/opt/local/bin/nmap"),
    ) -> None:
        """
        Initialize PortScanner module

        * detects nmap on the system and nmap version
        * may raise PortScannerError exception if nmap is not found in the path

        :param nmap_search_path: tupple of string where to search for nmap executable.
                                 Change this if you want to use a specific version of nmap.
        :returns: nothing

        """

    def get_nmap_last_output(self) -> str:
        """
        Returns the last text output of nmap in raw text
        this may be used for debugging purpose

        :returns: string containing the last text output of nmap in raw text
        """

    def nmap_version(self) -> tuple[int, int]:
        """
        returns nmap version if detected (int version, int subversion)
        or (0, 0) if unknown
        :returns: (nmap_version_number, nmap_subversion_number)
        """

    def listscan(self, hosts: str = "127.0.0.1") -> list[str]:
        """
        do not scan but interpret target hosts and return a list a hosts
        """

    def scan(
        self, hosts: str = "127.0.0.1", ports: str | None = None, arguments: str = "-sV", sudo: bool = False, timeout: int = 0
    ) -> _Result:
        """
        Scan given hosts

        May raise PortScannerError exception if nmap output was not xml

        Test existance of the following key to know
        if something went wrong : ['nmap']['scaninfo']['error']
        If not present, everything was ok.

        :param hosts: string for hosts as nmap use it 'scanme.nmap.org' or '198.116.0-255.1-127' or '216.163.128.20/20'
        :param ports: string for ports as nmap use it '22,53,110,143-4564'
        :param arguments: string of arguments for nmap '-sU -sX -sC'
        :param sudo: launch nmap with sudo if True
        :param timeout: int, if > zero, will terminate scan after seconds, otherwise will wait indefintely

        :returns: scan_result as dictionnary
        """

    def analyse_nmap_xml_scan(
        self,
        nmap_xml_output: str | None = None,
        nmap_err: str = "",
        nmap_err_keep_trace: str = "",
        nmap_warn_keep_trace: str = "",
    ) -> _Result:
        """
        Analyses NMAP xml scan ouput

        May raise PortScannerError exception if nmap output was not xml

        Test existance of the following key to know if something went wrong : ['nmap']['scaninfo']['error']
        If not present, everything was ok.

        :param nmap_xml_output: xml string to analyse
        :returns: scan_result as dictionnary
        """

    def __getitem__(self, host: str) -> PortScannerHostDict:
        """
        returns a host detail
        """

    def all_hosts(self) -> list[str]:
        """
        returns a sorted list of all hosts
        """

    def command_line(self) -> str:
        """
        returns command line used for the scan

        may raise AssertionError exception if called before scanning
        """

    def scaninfo(self) -> _ResultNmapInfo:
        """
        returns scaninfo structure
        {'tcp': {'services': '22', 'method': 'connect'}}

        may raise AssertionError exception if called before scanning
        """

    def scanstats(self) -> _ResultNampStats:
        """
        returns scanstats structure
        {'uphosts': '3', 'timestr': 'Thu Jun  3 21:45:07 2010', 'downhosts': '253', 'totalhosts': '256', 'elapsed': '5.79'}  # NOQA: E501

        may raise AssertionError exception if called before scanning
        """

    def has_host(self, host: str) -> bool:
        """
        returns True if host has result, False otherwise
        """

    def csv(self) -> str:
        """
        returns CSV output as text

        Example :
        host;hostname;hostname_type;protocol;port;name;state;product;extrainfo;reason;version;conf;cpe
        127.0.0.1;localhost;PTR;tcp;22;ssh;open;OpenSSH;protocol 2.0;syn-ack;5.9p1 Debian 5ubuntu1;10;cpe
        127.0.0.1;localhost;PTR;tcp;23;telnet;closed;;;conn-refused;;3;
        127.0.0.1;localhost;PTR;tcp;24;priv-mail;closed;;;conn-refused;;3;
        """

def __scan_progressive__(
    self: object, hosts: str, ports: str, arguments: str, callback: _Callback | None, sudo: bool, timeout: int
) -> None:
    """
    Used by PortScannerAsync for callback
    """

class PortScannerAsync:
    """
    PortScannerAsync allows to use nmap from python asynchronously
    for each host scanned, callback is called with scan result for the host

    """

    def __init__(self) -> None:
        """
        Initialize the module

        * detects nmap on the system and nmap version
        * may raise PortScannerError exception if nmap is not found in the path

        """

    def __del__(self) -> None:
        """
        Cleanup when deleted

        """

    def scan(
        self,
        hosts: str = "127.0.0.1",
        ports: str | None = None,
        arguments: str = "-sV",
        callback: _Callback | None = None,
        sudo: bool = False,
        timeout: int = 0,
    ) -> None:
        """
        Scan given hosts in a separate process and return host by host result using callback function

        PortScannerError exception from standard nmap is catched and you won't know about but get None as scan_data

        :param hosts: string for hosts as nmap use it 'scanme.nmap.org' or '198.116.0-255.1-127' or '216.163.128.20/20'
        :param ports: string for ports as nmap use it '22,53,110,143-4564'
        :param arguments: string of arguments for nmap '-sU -sX -sC'
        :param callback: callback function which takes (host, scan_data) as arguments
        :param sudo: launch nmap with sudo if true
        :param timeout: int, if > zero, will terminate scan after seconds, otherwise will wait indefintely

        """

    def stop(self) -> None:
        """
        Stop the current scan process

        """

    def wait(self, timeout: int | None = None) -> None:
        """
        Wait for the current scan process to finish, or timeout

        :param timeout: default = None, wait timeout seconds

        """

    def still_scanning(self) -> bool:
        """
        :returns: True if a scan is currently running, False otherwise

        """

class PortScannerYield(PortScannerAsync):
    """
    PortScannerYield allows to use nmap from python with a generator
    for each host scanned, yield is called with scan result for the host

    """

    def __init__(self) -> None:
        """
        Initialize the module

        * detects nmap on the system and nmap version
        * may raise PortScannerError exception if nmap is not found in the path

        """

    def scan(  # type: ignore[override]
        self, hosts: str = "127.0.0.1", ports: str | None = None, arguments: str = "-sV", sudo: bool = False, timeout: int = 0
    ) -> Iterator[tuple[str, _Result]]:
        """
        Scan given hosts in a separate process and return host by host result using callback function

        PortScannerError exception from standard nmap is catched and you won't know about it

        :param hosts: string for hosts as nmap use it 'scanme.nmap.org' or '198.116.0-255.1-127' or '216.163.128.20/20'
        :param ports: string for ports as nmap use it '22,53,110,143-4564'
        :param arguments: string of arguments for nmap '-sU -sX -sC'
        :param callback: callback function which takes (host, scan_data) as arguments
        :param sudo: launch nmap with sudo if true
        :param timeout: int, if > zero, will terminate scan after seconds, otherwise will wait indefintely

        """

    def stop(self) -> None: ...
    def wait(self, timeout: int | None = None) -> None: ...
    def still_scanning(self) -> None: ...  # type: ignore[override]

class PortScannerHostDict(dict[str, Any]):
    """
    Special dictionnary class for storing and accessing host scan result

    """

    def hostnames(self) -> list[_ResultHostNames]:
        """
        :returns: list of hostnames

        """

    def hostname(self) -> str:
        """
        For compatibility purpose...
        :returns: try to return the user record or the first hostname of the list hostnames

        """

    def state(self) -> str:
        """
        :returns: host state

        """

    def uptime(self) -> _ResulHostUptime:
        """
        :returns: host state

        """

    def all_protocols(self) -> list[str]:
        """
        :returns: a list of all scanned protocols

        """

    def all_tcp(self) -> list[int]:
        """
        :returns: list of tcp ports

        """

    def has_tcp(self, port: int) -> bool:
        """
        :param port: (int) tcp port
        :returns: True if tcp port has info, False otherwise

        """

    def tcp(self, port: int) -> _ResultHostPort:
        """
        :param port: (int) tcp port
        :returns: info for tpc port

        """

    def all_udp(self) -> list[int]:
        """
        :returns: list of udp ports

        """

    def has_udp(self, port: int) -> bool:
        """
        :param port: (int) udp port
        :returns: True if udp port has info, False otherwise

        """

    def udp(self, port: int) -> _ResultHostPort:
        """
        :param port: (int) udp port
        :returns: info for udp port

        """

    def all_ip(self) -> list[int]:
        """
        :returns: list of ip ports

        """

    def has_ip(self, port: int) -> bool:
        """
        :param port: (int) ip port
        :returns: True if ip port has info, False otherwise

        """

    def ip(self, port: int) -> _ResultHostPort:
        """
        :param port: (int) ip port
        :returns: info for ip port

        """

    def all_sctp(self) -> list[int]:
        """
        :returns: list of sctp ports

        """

    def has_sctp(self, port: int) -> bool:
        """
        :returns: True if sctp port has info, False otherwise

        """

    def sctp(self, port: int) -> _ResultHostPort:
        """
        :returns: info for sctp port

        """

class PortScannerError(Exception):
    """
    Exception error class for PortScanner class

    """

    value: str
    def __init__(self, value: str) -> None: ...

class PortScannerTimeout(PortScannerError): ...

def convert_nmap_output_to_encoding(value: _T, code: str = "ascii") -> _T:
    """
    Change encoding for scan_result object from unicode to whatever

    :param value: scan_result as dictionnary
    :param code: default = "ascii", encoding destination

    :returns: scan_result as dictionnary with new encoding
    """
