""" Constants for PolyMarket integration."""

from __future__ import annotations

from typing import Final

import logging

# Config
CONF_NAME = "name"
CONF_UNIQUE_ID = "unique_id"
CONF_REFRESH = "refresh"
CONF_LIMIT = "limit"
CONF_SCENES = "scenes"
CONF_SCENE_NAME = "name"
CONF_SCENE_TAG_SLUG = "tag_slug"
CONF_SCENE_EXCLUDE_TAG_IDS = "exclude_tag_ids"

#API
URL_HEAD = "http://gamma-api.polymarket.com"
URL_EVENTS = "/events?ascending=false&order=volume24hr&active=true&closed=false"

ATTRIBUTION = "Data provided by Polymarket"
DOMAIN: Final = "polymarket"

LOGGER = logging.getLogger(__package__)
