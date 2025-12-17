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

    def __init__(self, url: str) -> None:
        self._url: str = url
        self._session = None

    async def async_get_json(self) -> dict:
        """Get and Fetch the JSON data."""
        LOGGER.debug("Calling API: '%s'...", self._url)

        try:
            if self._session == None:
                self._session: ClientSession = aiohttp.ClientSession()

            async with self._session.get(self._url, headers=self.headers) as response:
                LOGGER.debug("Awaitng API response from %s...", self._url)

                result_json = await response.json()

                if response.status == HTTPStatus.OK:
                    return result_json
                else:
                    LOGGER.warn(
                        "Received status %d for %s, result=%s",
                        response.status,
                        self._url,
                        result_json)
        except Exception as e:
            self._session = None

            LOGGER.warn("API call failed: %s", e)

        return None
