""" Constants for PolyMarket integration."""

from __future__ import annotations

from typing import Final

import logging

# Config
CONF_LIMIT = "limit"
CONF_EXCLUDE_TAG_IDS = "exclude_tag_ids"

ATTRIBUTION = "Data provided by Polymarket"
DOMAIN: Final = "polymarket"

LOGGER = logging.getLogger(__package__)
