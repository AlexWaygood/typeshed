"""
Provide interface for persistent portable editable user settings
"""

from typing import Any, TypeVar

_S = TypeVar("_S")

class Settings(dict[str, Any]):
    """Provide interface for portable persistent user editable settings"""

    app_id: str
    settings_directory: str
    settings_file: str
    def __init__(self, app_id: str) -> None:
        """
        Create the settings object, using the specified app id (a reversed rfc
        1034 identifier, e.g. com.example.apps.thisapp
        """

    def add_setting(self, setting_name: str, setting_type: type[_S] = ..., default: _S | None = None) -> None:
        """Define a settings option (and default value)"""

    def load_settings(self) -> None:
        """Set default values and parse stored settings file"""

    def save_settings(self) -> None:
        """Write the settings data to disk"""

    def __getattr__(self, setting_name: str) -> Any:
        """Provide attribute-based access to stored config data"""

    def __setattr__(self, setting_name: str, setting_value: Any) -> None:
        """Provide attribute-based access to stored config data"""
