from collections.abc import MutableMapping
from logging import Logger
from typing import Any, Final, overload

log: Logger
SERVICE_NAME: Final[str]
ORIGIN: Final[str]
IMDS_URL: Final[str]

def initialize() -> None:
    """
    Try to get EC2 instance-id and AZ if running on EC2
    by querying http://169.254.169.254/latest/meta-data/.
    If not continue.
    """

def get_token() -> str | None:
    """
    Get the session token for IMDSv2 endpoint valid for 60 seconds
    by specifying the X-aws-ec2-metadata-token-ttl-seconds header.
    """

def get_metadata(token: str | None = None) -> dict[str, Any]: ...  # result of parse_metadata_json()
def parse_metadata_json(json_str: str | bytes | bytearray) -> dict[str, Any]: ...  # result of json.loads()
@overload
def do_request(url: str, headers: MutableMapping[str, str] | None = None, method: str = "GET") -> str: ...
@overload
def do_request(url: None, headers: MutableMapping[str, str] | None = None, method: str = "GET") -> None: ...
