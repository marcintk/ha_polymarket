""" API Query for PolyMarket integration."""

from __future__ import annotations
from homeassistant.config_entries import ConfigEntry

from .const import CONF_LIMIT, CONF_EXCLUDE_TAG_IDS, DOMAIN

URL_HEAD = "http://gamma-api.polymarket.com"
URL_EVENTS = "/events?ascending=false&order=volume24hr&active=true&closed=false"

class PolyMarketQuery:
    def __init__(self, entry: ConfigEntry):
        self._limit: int = entry[CONF_LIMIT]
        self._exclude_tag_ids: list[str] = entry[CONF_EXCLUDE_TAG_IDS]

    def name(self) -> str:
        return f"{DOMAIN}_news"

    def api_url(self) -> str:
        return URL_HEAD + URL_EVENTS + f"&limit={self._limit}" + self._excluded_tag_ids()

    def _excluded_tag_ids(self) -> str:
        ids = "&".join(map(lambda id : f"exclude_tag_id={id}", self._exclude_tag_ids))
        return f"&{ids}" if len(ids) > 0 else ""