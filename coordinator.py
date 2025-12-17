""" Coordinator for PolyMarket integration."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta, datetime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import PolymarketApi
from .const import DOMAIN, LOGGER
from .query import PolyMarketQuery
from .utils import parse_float_if, parse_float, parse_float_from_list_if, parse_float_from_list

SCAN_INTERVAL = 5

@dataclass
class EventsData:
    queryCount: int
    timestamp: datetime
    events: list[EventData] = field(default_factory=list)

    def append(self, event: EventData) -> None:
        return self.events.append(event)

@dataclass
class EventData:
    active: bool
    closed: bool
    title: str
    icon: str
    volume: float
    volume24hr: float
    liquidity: float
    endsAt: str
    updatedAt: str
    markets: list[MarketData] = field(default_factory=list)

@dataclass
class MarketData:
    active: bool
    closed: bool
    title: str
    icon: str
    volume: float
    volume24hr: float
    liquidity: float
    winPrice: float
    updatedAt: str


class PolyMarketDataUpdateCoordinator(DataUpdateCoordinator[EventsData]):
    def __init__(self, hass: HomeAssistant, query: PolyMarketQuery) -> None:
        self.queryCount: int = -100
        self.api: PolymarketApi = PolymarketApi(query.api_url())

        super().__init__(
            hass,
            logger=LOGGER,
            name=query.name(),
            update_interval=timedelta(minutes=SCAN_INTERVAL),
        )

        LOGGER.debug(f"Polymarket --init-- {self.name}")

    async def _async_setup(self) -> None:
        """Set up the coordinator

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        LOGGER.debug(f"Polymarket --_async_setup-- {self.name}")

        self.queryCount = 0

    async def _async_update_data(self) -> EventsData:
        """Do the usual update

        This method will be called automatically every SCAN_INTERVAL.
        """
        LOGGER.debug(f"Polymarket {self.name} --_async_update_data-- {self.queryCount}")

        self.queryCount += 1
        json_events = await self.api.async_get_json()

        data = EventsData(queryCount=self.queryCount, timestamp=datetime.now())

        for json_event in json_events:
            active = bool(json_event["active"])
            title=json_event["title"]
            markets = [self._update_market_data(item) for item in json_event["markets"]]
            markets = sorted(filter(lambda m: m.volume24hr>0, markets), key=lambda entry: entry.winPrice, reverse=True)

            data.append(EventData(
                active=active, 
                closed=bool(json_event["closed"]), 
                title=title, 
                icon=json_event["icon"], 
                volume=parse_float(json_event, "volume", root=title), 
                volume24hr=parse_float_if(active, json_event, "volume24hr", root=title), 
                liquidity=parse_float_if(active, json_event, "liquidity", root=title), 
                endsAt=json_event["endDate"], 
                updatedAt=json_event["updatedAt"], 
                markets=markets))

        return data

    def _update_market_data(self, json_market: dict) -> MarketData:
        active = bool(json_market["active"])
        title=json_market["groupItemTitle"]

        return MarketData(
            active=active, 
            closed=bool(json_market["closed"]), 
            title=title,
            icon=json_market["icon"], 
            volume=parse_float(json_market, "volume"), 
            volume24hr=parse_float_if(active, json_market, "volume24hr", root=title), 
            liquidity=parse_float_if(active, json_market, "liquidityNum", root=title), 
            winPrice=parse_float_from_list_if(active, json_market, "outcomePrices", root=title) * 100, 
            updatedAt=json_market["updatedAt"])
