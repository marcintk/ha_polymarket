""" API for PolyMarket integration."""

from __future__ import annotations

import aiohttp

from http import HTTPStatus

from .const import LOGGER

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/605.1.15 (KHTML, like "
    "Gecko) Version/15.0 Safari/605.1.15"
)

class PolymarketApi:
    headers: dict = {"User-Agent": USER_AGENT, "Accept": "application/ld+json"}

    def __init__(self) -> None:
        self._query_count: int = 0
        self._query_failed: int = 0
        self._session = None

    def query_count(self) -> int:
        return self._query_count

    def query_failed(self) -> int:
        return self._query_failed

    async def async_get_json(self, url: str) -> dict:
        """Get and Fetch the JSON data."""
        LOGGER.debug("Calling API: '%s'...", url)

        try:
            self._query_count += 1

            if self._session == None:
                self._session: ClientSession = aiohttp.ClientSession()

            async with self._session.get(url, headers=self.headers) as response:
                LOGGER.debug("Awaitng API response from %s...", url)

                result_json = await response.json()

                if response.status == HTTPStatus.OK:
                    return result_json
                else:
                    LOGGER.warning(
                        "Received status %d for %s, result=%s",
                        response.status,
                        url,
                        result_json)
        except Exception as e:
            self._session = None
            self._query_failed += 1

            LOGGER.warning("API call failed: %s", e)

        return None
