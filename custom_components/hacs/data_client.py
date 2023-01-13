"""HACS Data client."""
from __future__ import annotations

from typing import Any

from aiohttp import ClientSession, ClientTimeout

from .exceptions import HacsException


class HacsDataClient:
    """HACS Data client."""

    def __init__(self, session: ClientSession) -> None:
        """Initialize."""
        self.session = session

    async def _do_request(
        self,
        filename: str,
        section: str | None = None,
    ) -> dict[str, dict[str, Any]] | list[str]:
        """Do request."""
        endpoint = "/".join([v for v in [section, filename] if v is not None])
        try:
            response = await self.session.get(
                f"https://data-v2.hacs.xyz/{endpoint}",
                timeout=ClientTimeout(total=60),
            )
            response.raise_for_status()
        except Exception as exception:
            raise HacsException(f"Error fetching data from HACS: {exception}") from exception

        return await response.json()

    async def get_data(self, section: str | None) -> dict[str, dict[str, Any]]:
        """Get data."""
        return await self._do_request(filename="data.json", section=section)

    async def get_repositories(self, section: str) -> list[str]:
        """Get repositories."""
        return await self._do_request(filename="repositories.json", section=section)