"""NanoleafDigitalTwin

This module allows for the creation of a "digital twin", allowing you to
 make changes to individual panels and sync them to their real counterparts.
"""

from nanoleafapi.nanoleaf import Nanoleaf

class NanoleafDigitalTwin:
    """Class for creating and modifying digital twins

    :ivar nanoleaf: The Nanoleaf object
    :ivar tile_dict: The dictionary of tiles and their associated colour
    """

    nanoleaf: Nanoleaf
    tile_dict: dict[str, dict[str, int]]
    def __init__(self, nl: Nanoleaf) -> None:
        """Initialises a digital twin based on the Nanoleaf object provided.

        :param nl: The Nanoleaf object
        """

    def set_color(self, panel_id: int, rgb: tuple[int, int, int]) -> None:
        """Sets the colour of an individual panel.

        :param panel_id: The ID of the panel to change the colour of
        :param rgb: A tuple containing the RGB values of the colour to set
        """

    def set_all_colors(self, rgb: tuple[int, int, int]) -> None:
        """Sets the colour of all the panels.

        :param rgb: A tuple containing the RGB values of the colour to set
        """

    def get_ids(self) -> list[int]:
        """Returns a list of panel IDs.

        :returns: List of panel IDs.
        """

    def get_color(self, panel_id: int) -> tuple[int, int, int]:
        """Returns the colour of a specified panel.

        :param panel_id: The panel to get the colour of.

        :returns: Returns the RGB tuple of the panel with ID panel_id.
        """

    def get_all_colors(self) -> dict[int, tuple[int, int, int]]:
        """Returns a dictionary of all panel IDs and associated colours.

        :returns: Dictionary with panel IDs as keys and RGB tuples as values.
        """

    def sync(self) -> bool:
        """Syncs the digital twin's changes to the real Nanoleaf device.

        :returns: True if success, otherwise False
        """
