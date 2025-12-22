""" API Query for PolyMarket integration."""

from __future__ import annotations
from homeassistant.config_entries import ConfigEntry

from .const import (
    CONF_NAME,
    CONF_UNIQUE_ID,
    CONF_REFRESH,
    CONF_LIMIT,
    CONF_SCENES,
    CONF_SCENE_NAME,
    CONF_SCENE_TAG_SLUG,
    CONF_SCENE_EXCLUDE_TAG_IDS)

URL_HEAD = "http://gamma-api.polymarket.com"
URL_EVENTS = "/events?ascending=false&order=volume24hr&active=true"

class PolyMarketQueryScene:
    def __init__(self, scen: ConfigEntry):
        self._name: str = entry[CONF_SCENE_NAME]
        self._tag_slug: str = entry[CONF_SCENE_TAG_SLUG]
        self._exclude_tag_ids: list[str] = entry[CONF_EXCLUDE_TAG_IDS]

    def api_url(self) -> str:
        return f"&tag_slug={self._tag_slug}{self._excluded_tag_ids()}"

    def _excluded_tag_ids(self) -> str:
        if len(self._exclude_tag_ids) > 0:
            return "&" + "&".join(map(lambda id : f"exclude_tag_id={id}", self._exclude_tag_ids))
        return ""

class PolyMarketQuery:
    def __init__(self, entry: ConfigEntry):
        self._name: str = entry[CONF_NAME]"
        self._unique_id: str = entry[CONF_UNIQUE_ID]
        self._refresh_mins: int = entry[CONF_REFRESH]
        self._limit: int = entry[CONF_LIMIT]
        self._scenes: list[PolyMarketQueryScene] = [PolyMarketQueryScene(scene) for scene in entry[CONF_SCENES]]
        self._current: int = 0

    def name(self) -> str:
        return self._name

    def unique_id(self) -> str:
        return self._unique_id

    def refresh_mins(self) -> int:
        return self._refresh_mins

    def api_url(self, update_next: bool = false) -> str:
        url: str = URL_HEAD + URL_EVENTS + f"&limit={self._limit}" + self._scene(self._current)
        if update_next:
            self._current = (self._current + 1) % len(self._scenes)
        return url

    def _scene(self, id: int) -> str:
        if id < len(self._scenes):
            return self._scenes[id].api_url()
        return ''
