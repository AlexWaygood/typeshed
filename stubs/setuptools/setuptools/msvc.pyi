"""
Environment info about Microsoft Compilers.

>>> getfixture('windows_only')
>>> ei = EnvironmentInfo('amd64')
"""

import sys
from typing import Final, TypedDict, overload
from typing_extensions import LiteralString, NotRequired

if sys.platform == "win32":
    import winreg as winreg
    from os import environ as environ
else:
    class winreg:
        HKEY_USERS: Final[None]
        HKEY_CURRENT_USER: Final[None]
        HKEY_LOCAL_MACHINE: Final[None]
        HKEY_CLASSES_ROOT: Final[None]

    environ: dict[str, str]

class PlatformInfo:
    """
    Current and Target Architectures information.

    Parameters
    ----------
    arch: str
        Target architecture.
    """

    current_cpu: Final[str]

    arch: str

    def __init__(self, arch: str) -> None: ...
    @property
    def target_cpu(self) -> str:
        """
        Return Target CPU architecture.

        Return
        ------
        str
            Target CPU
        """

    def target_is_x86(self) -> bool:
        """
        Return True if target CPU is x86 32 bits..

        Return
        ------
        bool
            CPU is x86 32 bits
        """

    def current_is_x86(self) -> bool:
        """
        Return True if current CPU is x86 32 bits..

        Return
        ------
        bool
            CPU is x86 32 bits
        """

    def current_dir(self, hidex86: bool = False, x64: bool = False) -> str:
        """
        Current platform specific subfolder.

        Parameters
        ----------
        hidex86: bool
            return '' and not '\x86' if architecture is x86.
        x64: bool
            return 'd' and not '\x07md64' if architecture is amd64.

        Return
        ------
        str
            subfolder: '        arget', or '' (see hidex86 parameter)
        """

    def target_dir(self, hidex86: bool = False, x64: bool = False) -> str:
        """
        Target platform specific subfolder.

        Parameters
        ----------
        hidex86: bool
            return '' and not '\\x86' if architecture is x86.
        x64: bool
            return '\\x64' and not '\\amd64' if architecture is amd64.

        Return
        ------
        str
            subfolder: '\\current', or '' (see hidex86 parameter)
        """

    def cross_dir(self, forcex86: bool = False) -> str:
        """
        Cross platform specific subfolder.

        Parameters
        ----------
        forcex86: bool
            Use 'x86' as current architecture even if current architecture is
            not x86.

        Return
        ------
        str
            subfolder: '' if target architecture is current architecture,
            '\\current_target' if not.
        """

class RegistryInfo:
    """
    Microsoft Visual Studio related registry information.

    Parameters
    ----------
    platform_info: PlatformInfo
        "PlatformInfo" instance.
    """

    if sys.platform == "win32":
        HKEYS: Final[tuple[int, int, int, int]]
    else:
        HKEYS: Final[tuple[None, None, None, None]]

    pi: PlatformInfo

    def __init__(self, platform_info: PlatformInfo) -> None: ...
    @property
    def visualstudio(self) -> LiteralString:
        """
        Microsoft Visual Studio root registry key.

        Return
        ------
        str
            Registry key
        """

    @property
    def sxs(self) -> LiteralString:
        """
        Microsoft Visual Studio SxS registry key.

        Return
        ------
        str
            Registry key
        """

    @property
    def vc(self) -> LiteralString:
        """
        Microsoft Visual C++ VC7 registry key.

        Return
        ------
        str
            Registry key
        """

    @property
    def vs(self) -> LiteralString:
        """
        Microsoft Visual Studio VS7 registry key.

        Return
        ------
        str
            Registry key
        """

    @property
    def vc_for_python(self) -> LiteralString:
        """
        Microsoft Visual C++ for Python registry key.

        Return
        ------
        str
            Registry key
        """

    @property
    def microsoft_sdk(self) -> LiteralString:
        """
        Microsoft SDK registry key.

        Return
        ------
        str
            Registry key
        """

    @property
    def windows_sdk(self) -> LiteralString:
        """
        Microsoft Windows/Platform SDK registry key.

        Return
        ------
        str
            Registry key
        """

    @property
    def netfx_sdk(self) -> LiteralString:
        """
        Microsoft .NET Framework SDK registry key.

        Return
        ------
        str
            Registry key
        """

    @property
    def windows_kits_roots(self) -> LiteralString:
        """
        Microsoft Windows Kits Roots registry key.

        Return
        ------
        str
            Registry key
        """

    @overload
    def microsoft(self, key: LiteralString, x86: bool = False) -> LiteralString:
        """
        Return key in Microsoft software registry.

        Parameters
        ----------
        key: str
            Registry key path where look.
        x86: str
            Force x86 software registry.

        Return
        ------
        str
            Registry key
        """

    @overload
    def microsoft(self, key: str, x86: bool = False) -> str: ...  # type: ignore[misc]
    def lookup(self, key: str, name: str) -> str | None:
        """
        Look for values in registry in Microsoft software registry.

        Parameters
        ----------
        key: str
            Registry key path where look.
        name: str
            Value name to find.

        Return
        ------
        str
            value
        """

class SystemInfo:
    """
    Microsoft Windows and Visual Studio related system information.

    Parameters
    ----------
    registry_info: RegistryInfo
        "RegistryInfo" instance.
    vc_ver: float
        Required Microsoft Visual C++ version.
    """

    WinDir: Final[str]
    ProgramFiles: Final[str]
    ProgramFilesx86: Final[str]

    ri: RegistryInfo
    pi: PlatformInfo
    known_vs_paths: dict[float, str]
    vs_ver: float
    vc_ver: float

    def __init__(self, registry_info: RegistryInfo, vc_ver: float | None = None) -> None: ...
    def find_reg_vs_vers(self) -> list[float]:
        """
        Find Microsoft Visual Studio versions available in registry.

        Return
        ------
        list of float
            Versions
        """

    def find_programdata_vs_vers(self) -> dict[float, str]:
        """
        Find Visual studio 2017+ versions from information in
        "C:\\ProgramData\\Microsoft\\VisualStudio\\Packages\\_Instances".

        Return
        ------
        dict
            float version as key, path as value.
        """

    @property
    def VSInstallDir(self) -> str:
        """
        Microsoft Visual Studio directory.

        Return
        ------
        str
            path
        """

    @property
    def VCInstallDir(self) -> str:
        """
        Microsoft Visual C++ directory.

        Return
        ------
        str
            path
        """

    @property
    def WindowsSdkVersion(self) -> tuple[LiteralString, ...]:
        """
        Microsoft Windows SDK versions for specified MSVC++ version.

        Return
        ------
        tuple of str
            versions
        """

    @property
    def WindowsSdkLastVersion(self) -> str:
        """
        Microsoft Windows SDK last version.

        Return
        ------
        str
            version
        """

    @property
    def WindowsSdkDir(self) -> str | None:
        """
        Microsoft Windows SDK directory.

        Return
        ------
        str
            path
        """

    @property
    def WindowsSDKExecutablePath(self) -> str | None:
        """
        Microsoft Windows SDK executable directory.

        Return
        ------
        str
            path
        """

    @property
    def FSharpInstallDir(self) -> str:
        """
        Microsoft Visual F# directory.

        Return
        ------
        str
            path
        """

    @property
    def UniversalCRTSdkDir(self) -> str | None:
        """
        Microsoft Universal CRT SDK directory.

        Return
        ------
        str
            path
        """

    @property
    def UniversalCRTSdkLastVersion(self) -> str:
        """
        Microsoft Universal C Runtime SDK last version.

        Return
        ------
        str
            version
        """

    @property
    def NetFxSdkVersion(self) -> tuple[LiteralString, ...]:
        """
        Microsoft .NET Framework SDK versions.

        Return
        ------
        tuple of str
            versions
        """

    @property
    def NetFxSdkDir(self) -> str:
        """
        Microsoft .NET Framework SDK directory.

        Return
        ------
        str
            path
        """

    @property
    def FrameworkDir32(self) -> str:
        """
        Microsoft .NET Framework 32bit directory.

        Return
        ------
        str
            path
        """

    @property
    def FrameworkDir64(self) -> str:
        """
        Microsoft .NET Framework 64bit directory.

        Return
        ------
        str
            path
        """

    @property
    def FrameworkVersion32(self) -> tuple[str, ...]:
        """
        Microsoft .NET Framework 32bit versions.

        Return
        ------
        tuple of str
            versions
        """

    @property
    def FrameworkVersion64(self) -> tuple[str, ...]:
        """
        Microsoft .NET Framework 64bit versions.

        Return
        ------
        tuple of str
            versions
        """

class _EnvironmentDict(TypedDict):
    include: str
    lib: str
    libpath: str
    path: str
    py_vcruntime_redist: NotRequired[str | None]

class EnvironmentInfo:
    """
    Return environment variables for specified Microsoft Visual C++ version
    and platform : Lib, Include, Path and libpath.

    This function is compatible with Microsoft Visual C++ 9.0 to 14.X.

    Script created by analysing Microsoft environment configuration files like
    "vcvars[...].bat", "SetEnv.Cmd", "vcbuildtools.bat", ...

    Parameters
    ----------
    arch: str
        Target architecture.
    vc_ver: float
        Required Microsoft Visual C++ version. If not set, autodetect the last
        version.
    vc_min_ver: float
        Minimum Microsoft Visual C++ version.
    """

    pi: PlatformInfo
    ri: RegistryInfo
    si: SystemInfo

    def __init__(self, arch: str, vc_ver: float | None = None, vc_min_ver: float = 0) -> None: ...
    @property
    def vs_ver(self) -> float:
        """
        Microsoft Visual Studio.

        Return
        ------
        float
            version
        """

    @property
    def vc_ver(self) -> float:
        """
        Microsoft Visual C++ version.

        Return
        ------
        float
            version
        """

    @property
    def VSTools(self) -> list[str]:
        """
        Microsoft Visual Studio Tools.

        Return
        ------
        list of str
            paths
        """

    @property
    def VCIncludes(self) -> list[str]:
        """
        Microsoft Visual C++ & Microsoft Foundation Class Includes.

        Return
        ------
        list of str
            paths
        """

    @property
    def VCLibraries(self) -> list[str]:
        """
        Microsoft Visual C++ & Microsoft Foundation Class Libraries.

        Return
        ------
        list of str
            paths
        """

    @property
    def VCStoreRefs(self) -> list[str]:
        """
        Microsoft Visual C++ store references Libraries.

        Return
        ------
        list of str
            paths
        """

    @property
    def VCTools(self) -> list[str]:
        """
        Microsoft Visual C++ Tools.

        Return
        ------
        list of str
            paths

        When host CPU is ARM, the tools should be found for ARM.

        >>> getfixture('windows_only')
        >>> mp = getfixture('monkeypatch')
        >>> mp.setattr(PlatformInfo, 'current_cpu', 'arm64')
        >>> ei = EnvironmentInfo(arch='irrelevant')
        >>> paths = ei.VCTools
        >>> any('HostARM64' in path for path in paths)
        True
        """

    @property
    def OSLibraries(self) -> list[str]:
        """
        Microsoft Windows SDK Libraries.

        Return
        ------
        list of str
            paths
        """

    @property
    def OSIncludes(self) -> list[str]:
        """
        Microsoft Windows SDK Include.

        Return
        ------
        list of str
            paths
        """

    @property
    def OSLibpath(self) -> list[str]:
        """
        Microsoft Windows SDK Libraries Paths.

        Return
        ------
        list of str
            paths
        """

    @property
    def SdkTools(self) -> list[str]:
        """
        Microsoft Windows SDK Tools.

        Return
        ------
        list of str
            paths
        """

    @property
    def SdkSetup(self) -> list[str]:
        """
        Microsoft Windows SDK Setup.

        Return
        ------
        list of str
            paths
        """

    @property
    def FxTools(self) -> list[str]:
        """
        Microsoft .NET Framework Tools.

        Return
        ------
        list of str
            paths
        """

    @property
    def NetFxSDKLibraries(self) -> list[str]:
        """
        Microsoft .Net Framework SDK Libraries.

        Return
        ------
        list of str
            paths
        """

    @property
    def NetFxSDKIncludes(self) -> list[str]:
        """
        Microsoft .Net Framework SDK Includes.

        Return
        ------
        list of str
            paths
        """

    @property
    def VsTDb(self) -> list[str]:
        """
        Microsoft Visual Studio Team System Database.

        Return
        ------
        list of str
            paths
        """

    @property
    def MSBuild(self) -> list[str]:
        """
        Microsoft Build Engine.

        Return
        ------
        list of str
            paths
        """

    @property
    def HTMLHelpWorkshop(self) -> list[str]:
        """
        Microsoft HTML Help Workshop.

        Return
        ------
        list of str
            paths
        """

    @property
    def UCRTLibraries(self) -> list[str]:
        """
        Microsoft Universal C Runtime SDK Libraries.

        Return
        ------
        list of str
            paths
        """

    @property
    def UCRTIncludes(self) -> list[str]:
        """
        Microsoft Universal C Runtime SDK Include.

        Return
        ------
        list of str
            paths
        """

    @property
    def FSharp(self) -> list[str]:
        """
        Microsoft Visual F#.

        Return
        ------
        list of str
            paths
        """

    @property
    def VCRuntimeRedist(self) -> str | None:
        """
        Microsoft Visual C++ runtime redistributable dll.

        Returns the first suitable path found or None.
        """

    def return_env(self, exists: bool = True) -> _EnvironmentDict:
        """
        Return environment dict.

        Parameters
        ----------
        exists: bool
            It True, only return existing paths.

        Return
        ------
        dict
            environment
        """
