from consolemenu.validators.base import BaseValidator as BaseValidator

class UrlValidator(BaseValidator):
    def __init__(self) -> None:
        """
        URL Validator class
        """

    def validate(self, input_string: str) -> bool:
        """
        Validate url

        :return: True if match / False otherwise
        """
