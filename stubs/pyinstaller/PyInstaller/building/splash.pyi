from _typeshed import StrPath

from PyInstaller.building.datastruct import Target, _TOCTuple

splash_requirements: list[str]

# Referenced in https://pyinstaller.org/en/stable/spec-files.html#example-merge-spec-file
# Not to be imported during runtime, but is the type reference for spec files which are executed as python code
class Splash(Target):
    """
    Bundles the required resources for the splash screen into a file, which will be included in the CArchive.

    A Splash has two outputs, one is itself and one is stored in splash.binaries. Both need to be passed to other
    build targets in order to enable the splash screen.
    """

    image_file: str
    full_tk: bool
    tcl_lib: str
    tk_lib: str
    name: str
    script_name: StrPath
    minify_script: bool
    max_img_size: tuple[int, int]
    text_pos: tuple[int, int] | None
    text_size: int
    text_font: str
    text_color: str
    text_default: str
    always_on_top: bool
    uses_tkinter: bool
    script: str
    splash_requirements: set[str]
    binaries: list[_TOCTuple]
    def __init__(
        self,
        image_file: StrPath,
        binaries: list[_TOCTuple],
        datas: list[_TOCTuple],
        *,
        text_pos: tuple[int, int] | None = ...,
        text_size: int = 12,
        text_font: str = ...,
        text_color: str = "black",
        text_default: str = "Initializing",
        full_tk: bool = False,
        minify_script: bool = True,
        name: str = ...,
        script_name: StrPath = ...,
        max_img_size: tuple[int, int] | None = (760, 480),
        always_on_top: bool = True,
    ) -> None:
        """
        :param str image_file:
            A path-like object to the image to be used. Only the PNG file format is supported.

            .. note:: If a different file format is supplied and PIL (Pillow) is installed, the file will be converted
                automatically.

            .. note:: *Windows*: The color ``'magenta'`` / ``'#ff00ff'`` must not be used in the image or text, as it is
                used by splash screen to indicate transparent areas. Use a similar color (e.g., ``'#ff00fe'``) instead.

            .. note:: If PIL (Pillow) is installed and the image is bigger than max_img_size, the image will be resized
                to fit into the specified area.
        :param list binaries:
            The TOC list of binaries the Analysis build target found. This TOC includes all extension modules and their
            binary dependencies. This is required to determine whether the user's program uses `tkinter`.
        :param list datas:
            The TOC list of data the Analysis build target found. This TOC includes all data-file dependencies of the
            modules. This is required to check if all splash screen requirements can be bundled.

        :keyword text_pos:
            An optional two-integer tuple that represents the origin of the text on the splash screen image. The
            origin of the text is its lower left corner. A unit in the respective coordinate system is a pixel of the
            image, its origin lies in the top left corner of the image. This parameter also acts like a switch for
            the text feature. If omitted, no text will be displayed on the splash screen. This text will be used to
            show textual progress in onefile mode.
        :type text_pos: Tuple[int, int]
        :keyword text_size:
            The desired size of the font. If the size argument is a positive number, it is interpreted as a size in
            points. If size is a negative number, its absolute value is interpreted as a size in pixels. Default: ``12``
        :type text_size: int
        :keyword text_font:
            An optional name of a font for the text. This font must be installed on the user system, otherwise the
            system default font is used. If this parameter is omitted, the default font is also used.
        :keyword text_color:
            An optional color for the text. HTML color codes (``'#40e0d0'``) and color names (``'turquoise'``) are
            supported. Default: ``'black'``
            (Windows: the color ``'magenta'`` / ``'#ff00ff'`` is used to indicate transparency, and should not be used)
        :type text_color: str
        :keyword text_default:
            The default text which will be displayed before the extraction starts. Default: ``"Initializing"``
        :type text_default: str
        :keyword full_tk:
            By default Splash bundles only the necessary files for the splash screen (some tk components). This
            options enables adding full tk and making it a requirement, meaning all tk files will be unpacked before
            the splash screen can be started. This is useful during development of the splash screen script.
            Default: ``False``
        :type full_tk: bool
        :keyword minify_script:
            The splash screen is created by executing an Tcl/Tk script. This option enables minimizing the script,
            meaning removing all non essential parts from the script. Default: ``True``
        :keyword name:
            An optional alternative filename for the .res file. If not specified, a name is generated.
        :type name: str
        :keyword script_name:
            An optional alternative filename for the Tcl script, that will be generated. If not specified, a name is
            generated.
        :type script_name: str
        :keyword max_img_size:
            Maximum size of the splash screen image as a tuple. If the supplied image exceeds this limit, it will be
            resized to fit the maximum width (to keep the original aspect ratio). This option can be disabled by
            setting it to None. Default: ``(760, 480)``
        :type max_img_size: Tuple[int, int]
        :keyword always_on_top:
            Force the splashscreen to be always on top of other windows. If disabled, other windows (e.g., from other
            applications) can cover the splash screen by user bringing them to front. This might be useful for
            frozen applications with long startup times. Default: ``True``
        :type always_on_top: bool
        """

    def assemble(self) -> None: ...
    def generate_script(self) -> str:
        """
        Generate the script for the splash screen.

        If minify_script is True, all unnecessary parts will be removed.
        """
