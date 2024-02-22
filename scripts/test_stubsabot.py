import asyncio

import aiohttp
from stubsabot import fetch_pypi_info, release_contains_py_typed

py_typed_packages = [
    #    "mypy",
    "Flask-SQLAlchemy",
    "SQLAlchemy",
    "typeshed-stats",
    "urllib3",
    "annoy",
    "freezegun",
    "certifi",
    "cryptography",
    "selenium",
    "emoji",
    "dj-database-url",
    #    "pyvmomi",
    "invoke",
    "babel",
    "chardet",
    "prettytable",
    "termcolor",
    "xxhash",
    "orjson",
    "attrs",
]


async def check_package_detected_as_py_typed(distribution: str, session: aiohttp.ClientSession) -> None:
    pypi_info = await fetch_pypi_info(distribution, session=session)
    latest_release = next(release for release in pypi_info.releases_in_descending_order() if not release.version.is_prerelease)
    assert await release_contains_py_typed(latest_release, session=session), distribution


async def check_all_packages() -> None:
    async with aiohttp.ClientSession() as session:
        tasks = (check_package_detected_as_py_typed(package, session) for package in py_typed_packages)
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(check_all_packages())
