"""nanoleafapi

This module is a Python 3 wrapper for the Nanoleaf OpenAPI.
It provides an easy way to use many of the functions available in the API.
It supports the Light Panels (previously Aurora), Canvas and Shapes (including Hexgaons).
"""

from _typeshed import Incomplete
from collections.abc import Callable
from typing import Any

RED: tuple[int, int, int]
ORANGE: tuple[int, int, int]
YELLOW: tuple[int, int, int]
GREEN: tuple[int, int, int]
LIGHT_BLUE: tuple[int, int, int]
BLUE: tuple[int, int, int]
PINK: tuple[int, int, int]
PURPLE: tuple[int, int, int]
WHITE: tuple[int, int, int]

class Nanoleaf:
    """The Nanoleaf class for controlling the Light Panels and Canvas

    :ivar ip: IP of the Nanoleaf device
    :ivar url: The base URL for requests
    :ivar auth_token: The authentication token for the API
    :ivar print_errors: True for errors to be shown, otherwise False
    """

    ip: str
    print_errors: bool
    url: str
    auth_token: str
    already_registered: bool
    def __init__(self, ip: str, auth_token: str | None = None, print_errors: bool = False) -> None:
        """Initalises Nanoleaf class with desired arguments.

        :param ip: The IP address of the Nanoleaf device
        :param auth_token: Optional, include Nanoleaf authentication
            token here if required.
        :param print_errors: Optional, True to show errors in the console

        :type ip: str
        :type auth_token: str
        :type print_errors: bool
        """

    def create_auth_token(self) -> str | None:
        """Creates or retrives the device authentication token

        The power button on the device should be held for 5-7 seconds, then
        this method should be run. This will set both the auth_token and url
        instance variables, and save the token in a file for future instances
        of the Nanoleaf object.

        :returns: Token if successful, None if not.
        """

    def delete_auth_token(self, auth_token: str) -> bool:
        """Deletes an authentication token

        Deletes an authentication token and the .nanoleaf_token file if it
        contains the auth token to delete. This token can no longer be used
        as part of an API call to control the device. If required, generate
        a new one using create_auth_token().

        :param auth_token: The authentication token to delete.

        :returns: True if successful, otherwise False
        """

    def check_connection(self) -> None:
        """Ensures there is a valid connection"""

    def get_info(self) -> dict[str, Incomplete]:
        """Returns a dictionary of device information"""

    def get_name(self) -> str:
        """Returns the name of the current device"""

    def get_auth_token(self) -> str | None:
        """Returns the current auth token or None"""

    def get_ids(self) -> list[int]:
        """Returns a list of all device ids"""

    @staticmethod
    def get_custom_base_effect(anim_type: str = "custom", loop: bool = True) -> dict[str, Incomplete]:
        """Returns base custom effect dictionary"""

    def power_off(self) -> bool:
        """Powers off the lights

        :returns: True if successful, otherwise False
        """

    def power_on(self) -> bool:
        """Powers on the lights

        :returns: True if successful, otherwise False
        """

    def get_power(self) -> bool:
        """Returns the power status of the lights

        :returns: True if on, False if off
        """

    def toggle_power(self) -> bool:
        """Toggles the lights on/off"""

    def set_color(self, rgb: tuple[int, int, int]) -> bool:
        """Sets the colour of the lights

        :param rgb: Tuple in the format (r, g, b)

        :returns: True if successful, otherwise False
        """

    def set_brightness(self, brightness: int, duration: int = 0) -> bool:
        """Sets the brightness of the lights

        :param brightness: The required brightness (between 0 and 100)
        :param duration: The duration over which to change the brightness

        :returns: True if successful, otherwise False
        """

    def increment_brightness(self, brightness: int) -> bool:
        """Increments the brightness of the lights

        :param brightness: How much to increment the brightness, can
            also be negative

        :returns: True if successful, otherwise False
        """

    def get_brightness(self) -> int:
        """Returns the current brightness value of the lights"""

    def identify(self) -> bool:
        """Runs the identify sequence on the lights

        :returns: True if successful, otherwise False
        """

    def set_hue(self, value: int) -> bool:
        """Sets the hue of the lights

        :param value: The required hue (between 0 and 360)

        :returns: True if successful, otherwise False
        """

    def increment_hue(self, value: int) -> bool:
        """Increments the hue of the lights

        :param value: How much to increment the hue, can also be negative

        :returns: True if successful, otherwise False
        """

    def get_hue(self) -> int:
        """Returns the current hue value of the lights"""

    def set_saturation(self, value: int) -> bool:
        """Sets the saturation of the lights

        :param value: The required saturation (between 0 and 100)

        :returns: True if successful, otherwise False
        """

    def increment_saturation(self, value: int) -> bool:
        """Increments the saturation of the lights

        :param brightness: How much to increment the saturation, can also be
            negative.

        :returns: True if successful, otherwise False
        """

    def get_saturation(self) -> int:
        """Returns the current saturation value of the lights"""

    def set_color_temp(self, value: int) -> bool:
        """Sets the white colour temperature of the lights

        :param value: The required colour temperature (between 0 and 100)

        :returns: True if successful, otherwise False
        """

    def increment_color_temp(self, value: int) -> bool:
        """Sets the white colour temperature of the lights

        :param value: How much to increment the colour temperature by, can also
            be negative.

        :returns: True if successful, otherwise False
        """

    def get_color_temp(self) -> int:
        """Returns the current colour temperature of the lights"""

    def get_color_mode(self) -> str:
        """Returns the colour mode of the lights"""

    def get_current_effect(self) -> str:
        """Returns the currently selected effect

        If the name of the effect isn't available, this will return
        *Solid*, *Dynamic* or *Static* instead.

        :returns: Name of the effect or type if unavailable.
        """

    def set_effect(self, effect_name: str) -> bool:
        """Sets the effect of the lights

        :param effect_name: The name of the effect

        :returns: True if successful, otherwise False
        """

    def list_effects(self) -> list[str]:
        """Returns a list of available effects"""

    def write_effect(self, effect_dict: dict[str, Incomplete]) -> bool:
        """Writes a user-defined effect to the panels

        :param effect_dict: The effect dictionary in the format
            described here: https://forum.nanoleaf.me/docs/openapi#_u2t4jzmkp8nt

        :raises NanoleafEffectCreationError: When invalid effect dictionary is provided.

        :returns: True if successful, otherwise False
        """

    def effect_exists(self, effect_name: str) -> bool:
        """Verifies whether an effect exists

        :param effect_name: Name of the effect to verify

        :returns: True if effect exists, otherwise False
        """

    def pulsate(self, rgb: tuple[int, int, int], speed: float = 1) -> bool:
        """Displays a pulsating effect on the device with two colours

        :param rgb: A tuple containing the RGB colour to pulsate in the format (r, g, b).
        :param speed: The speed of the transition between colours in seconds,
            with a maximum of 1 decimal place.

        :raises NanoleafEffectCreationError: When an invalid rgb value is provided.

        :returns: True if the effect was created and displayed successfully, otherwise False
        """

    def flow(self, rgb_list: list[tuple[int, int, int]], speed: float = 1) -> bool:
        """Displays a sequence of specified colours on the device.

        :param rgb: A list of tuples containing RGB colours to flow between in the format (r, g, b).
        :param speed: The speed of the transition between colours in seconds, with a maximum of
            1 decimal place.

        :raises NanoleafEffectCreationError: When an invalid rgb_list is provided.

        :returns: True if the effect was created and displayed successfully, otherwise False
        """

    def spectrum(self, speed: float = 1) -> bool:
        """Displays a spectrum cycling effect on the device

        :param speed: The speed of the transition between colours in seconds,
            with a maximum of 1 decimal place.

        :returns: True if the effect was created and displayed successfully,
            otherwise False
        """

    def enable_extcontrol(self) -> bool:
        """Enables the extControl UDP streaming mode

        :returns: True if successful, otherwise False
        """

    def get_layout(self) -> dict[str, Incomplete]:
        """Returns the device layout information"""

    def register_event(self, func: Callable[[dict[str, Incomplete]], Any], event_types: list[int]) -> None:
        """Starts a thread to register and listen for events

        Creates an event listener. This method can only be called once per
        program run due to API limitations.

        :param func: The function to run when an event is recieved (this
            should be defined by the user with one argument). This function
            will recieve the event as a dictionary.
        :param event_types: A list containing up to 4 numbers from
            1-4 corresponding to the relevant events to be registered for.
            1 = state (power/brightness),
            2 = layout,
            3 = effects,
            4 = touch (Canvas only)
        """

class NanoleafRegistrationError(Exception):
    """Raised when an issue during device registration."""

    def __init__(self) -> None: ...

class NanoleafConnectionError(Exception):
    """Raised when the connection to the Nanoleaf device fails."""

    def __init__(self) -> None: ...

class NanoleafEffectCreationError(Exception):
    """Raised when one of the custom effects creation has incorrect arguments."""
