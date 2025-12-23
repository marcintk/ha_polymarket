""" Coordinator for PolyMarket integration."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta, datetime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import PolymarketApi
from .const import LOGGER
from .query import PolyMarketQuery
from .utils import parse_str, parse_str_if, parse_float_if, parse_float, parse_float_from_list_if, parse_float_from_list

@dataclass
class EventsData:
    scene: str
    query_count: int
    query_failed: int
    query_url: str
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
    volume_24hr: float
    liquidity: float
    ends_at: str
    updated_at: str
    markets: list[MarketData] = field(default_factory=list)

@dataclass
class MarketData:
    active: bool
    closed: bool
    title: str
    icon: str
    volume: float
    volume_24hr: float
    liquidity: float
    win_price: float
    updated_at: str


class PolyMarketDataUpdateCoordinator(DataUpdateCoordinator[EventsData]):
    def __init__(self, hass: HomeAssistant, query: PolyMarketQuery) -> None:
        self._query: PolyMarketQuery = query
        self._api: PolymarketApi = PolymarketApi()

        super().__init__(
            hass,
            logger=LOGGER,
            name=query.name(),
            update_interval=timedelta(minutes=query.refresh_mins()),
        )

        LOGGER.debug(f"Polymarket --init-- {self.name}")

    async def _async_setup(self) -> None:
        """Set up the coordinator

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        LOGGER.debug(f"Polymarket --_async_setup-- {self.name}")

    async def _async_update_data(self) -> EventsData:
        """Do the usual update

        This method will be called automatically every SCAN_INTERVAL.
        """
        LOGGER.debug(f"Polymarket {self.name} --_async_update_data-- {self._api.query_count()}")

        scene, url = self._query.api_url(update_next=True)
        json_events: dict = await PolymarketApi().async_get_json(url)

        data = EventsData(
            scene=scene,
            query_count=self._api.query_count(),
            query_failed=self._api.query_failed(),
            query_url=url, 
            timestamp=datetime.now())

        for json_event in json_events:
            active = bool(json_event["active"])
            endsAt = parse_str(json_event, "endDate", default=None)

            if active and endsAt is not None:
                title = json_event["title"]
                markets = [self._update_market_data(item) for item in json_event["markets"]]
                markets = sorted(filter(lambda m: m.volume_24hr>0, markets), key=lambda entry: entry.win_price, reverse=True)

                data.append(EventData(
                    active=active,
                    closed=bool(json_event["closed"]),
                    title=title,
                    icon=json_event["icon"],
                    volume=parse_float(json_event, "volume", root=title),
                    volume_24hr=parse_float_if(active, json_event, "volume24hr", root=title),
                    liquidity=parse_float_if(active, json_event, "liquidity", root=title),
                    ends_at=parse_str(json_event, "endDate", default=None),
                    updated_at=json_event["updatedAt"],
                    markets=markets))

        return data

    def _update_market_data(self, json_market: dict) -> MarketData:
        active = bool(json_market["active"])
        title = parse_str(json_market, "groupItemTitle")

        return MarketData(
            active=active, 
            closed=bool(json_market["closed"]), 
            title=title,
            icon=json_market["icon"], 
            volume=parse_float(json_market, "volume"), 
            volume_24hr=parse_float_if(active, json_market, "volume24hr", root=title), 
            liquidity=parse_float_if(active, json_market, "liquidityNum", root=title), 
            win_price=parse_float_from_list_if(active, json_market, "outcomePrices", root=title) * 100, 
            updated_at=json_market["updatedAt"])
