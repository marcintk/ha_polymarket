"""Platform for PolyMarket integration."""

from __future__ import annotations

import voluptuous as vol

# Import the device class from the component that you want to support

from datetime import datetime
from homeassistant.components.sensor import SensorEntity, PLATFORM_SCHEMA
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from typing import Any, Final

from .coordinator import PolyMarketDataUpdateCoordinator, EventsData, EventData, MarketData
from .const import (
    ATTRIBUTION,
    CONF_NAME,
    CONF_UNIQUE_ID,
    CONF_REFRESH,
    CONF_LIMIT,
    CONF_SCENES,
    CONF_SCENE_NAME,
    CONF_SCENE_TAG_SLUG,
    CONF_SCENE_EXCLUDE_TAG_IDS,
    DOMAIN,
    LOGGER
)
from .query import PolyMarketQuery

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_UNIQUE_ID): cv.string,
    vol.Optional(CONF_REFRESH, default=5): vol.Coerce(int),
    vol.Optional(CONF_LIMIT, default=5): vol.Coerce(int),
    vol.Optional(CONF_SCENES, default=[]): vol.All(
        cv.ensure_list,
        [vol.Schema({
            vol.Required(CONF_SCENE_NAME): cv.string,
            vol.Optional(CONF_SCENE_TAG_SLUG): cv.string,
            vol.Optional(CONF_SCENE_EXCLUDE_TAG_IDS, default=[]): vol.All(
                cv.ensure_list,
                [cv.string],
            ),
        })]
    ),
})

async def async_setup_platform(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
):
    """Set up the Polymarket sensor platform."""

    LOGGER.debug(f"Polymarket --sensor-- {entry}")

    # This gets the data update coordinator from the config entry runtime data as specified in your __init__.py
    #coordinator: PolyMarketDataUpdateCoordinator = entry.runtime_data.coordinator

    query = PolyMarketQuery(entry)

    coordinator = PolyMarketDataUpdateCoordinator(hass, query)
    await coordinator.async_refresh()

    sensor = PolymarketSensor(coordinator, query.name(), query.unique_id())
    async_add_entities([sensor], update_before_add=False)

    LOGGER.info(f"Polymarket sensor addd: {query}.")


class PolymarketSensor(CoordinatorEntity[PolyMarketDataUpdateCoordinator], SensorEntity):
    """Representation of an Polymarket."""

    def __init__(self, coordinator: PolyMarketDataUpdateCoordinator, name: str, unique_id: str) -> None:
        """Initialize an Polymarket."""
        super().__init__(coordinator)
        self._name: str = name
        self._unique_id: str = unique_id

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._unique_id

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state message."""

        data: EventsData = self.coordinator.data

        attrs = {}
        attrs[ATTR_ATTRIBUTION] = ATTRIBUTION
        attrs["domain"] = DOMAIN
        attrs["scene"] = data.scene
        attrs["url"] = data.query_url
        attrs["queryCount"] = data.query_count
        attrs["timestamp"] = data.timestamp

        events = []
        for event in data.events:
            event_attrs = {}
            event_attrs["active"] = event.active
            event_attrs["closed"] = event.closed
            event_attrs["title"] = event.title
            event_attrs["icon"] = event.icon
            event_attrs["volume"] = event.volume
            event_attrs["volume24hr"] = event.volume_24hr
            event_attrs["liquidity"] = event.liquidity
            event_attrs["endsAt"] = event.ends_at
            event_attrs["updatedAt"] = event.updated_at

            markets = []
            for market in event.markets:
                market_attrs = {}
                market_attrs["active"] = market.active
                market_attrs["closed"] = market.closed
                market_attrs["title"] = market.title
                market_attrs["volume"] = market.volume
                market_attrs["volume24hr"] = market.volume_24hr
                market_attrs["liquidity"] = market.liquidity
                market_attrs["winPrice"] = market.win_price
                market_attrs["updatedAt"] = market.updated_at
                markets.append(market_attrs)

            event_attrs["markets"] = markets
            events.append(event_attrs)

        attrs["events"] = events

        return attrs