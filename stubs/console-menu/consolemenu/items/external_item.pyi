from consolemenu.items import MenuItem as MenuItem

class ExternalItem(MenuItem):
    """
    A base class for items that need to do stuff on the console outside of the console menu.
    Sets the terminal back to standard mode until the action is done.
    Should probably be subclassed.
    """

    def set_up(self) -> None:
        """
        This class overrides this method
        """

    def clean_up(self) -> None:
        """
        This class overrides this method
        """
