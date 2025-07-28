from collections.abc import Iterable
from logging import Logger

log: Logger
SUPPORTED_MODULES: tuple[str, ...]
NO_DOUBLE_PATCH: tuple[str, ...]

def patch_all(double_patch: bool = False) -> None:
    """
    The X-Ray Python SDK supports patching aioboto3, aiobotocore, boto3, botocore, pynamodb, requests,
    sqlite3, mysql, httplib, pymongo, pymysql, psycopg2, pg8000, sqlalchemy_core, httpx, and mysql-connector.

    To patch all supported libraries::

        from aws_xray_sdk.core import patch_all

        patch_all()

    :param bool double_patch: enable or disable patching of indirect dependencies.
    """

def patch(
    modules_to_patch: Iterable[str], raise_errors: bool = True, ignore_module_patterns: Iterable[str] | None = None
) -> None:
    """
    To patch specific modules::

        from aws_xray_sdk.core import patch

        i_want_to_patch = ('botocore') # a tuple that contains the libs you want to patch
        patch(i_want_to_patch)

    :param tuple modules_to_patch: a tuple containing the list of libraries to be patched
    """
