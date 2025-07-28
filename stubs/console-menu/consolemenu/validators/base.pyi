import abc
from abc import abstractmethod
from logging import Logger

class InvalidValidator(Exception):
    """
    Raised when expected a valid validator but something else given
    """

class BaseValidator(metaclass=abc.ABCMeta):
    """
    Validator Base class, each validator should inherit from this one
    """

    log: Logger
    def __init__(self) -> None: ...
    @abstractmethod
    def validate(self, input_string: str) -> bool:
        """

        This function should be implemented in the validators

        :param input_string: Input string from command line (provided by the user)
        :return: True in case validation success / False otherwise
        """
