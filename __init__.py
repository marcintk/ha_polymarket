"""The Detailed PolyMarket integration."""

# from __future__ import annotations
# from homeassistant.config_entries import ConfigEntry

# from dataclasses import dataclass
# from homeassistant.core import HomeAssistant
# from homeassistant.const import Platform

# from .coordinator import PolyMarketDataUpdateCoordinator
# from .const import LOGGER

# type PolyMarketConfigEntry = ConfigEntry[PolyMarketDataUpdateCoordinator]

# # List of platforms to support. There should be a matching .py file for each,
# # eg <cover.py> and <sensor.py>
# PLATFORMS: list[Platform] = [Platform.SENSOR]

# type MyConfigEntry = ConfigEntry[RuntimeData]

# @dataclass
# class RuntimeData:
#     """Class to hold your data."""

#     coordinator: DataUpdateCoordinator

# async def async_setup_entry(hass: HomeAssistant, entry: MyConfigEntry) -> bool:
#     """Set up the component."""
#     LOGGER.warn(f"Polymarket --async_setup_entry-- {entry}")

#     coordinator = PolyMarketSlugDataUpdateCoordinator(hass, entry[CONF_SLUG_NAME])

#     # ensure it is setup
#     await coordinator.async_refresh()

#     # Add the coordinator and update listener to config runtime data to make
#     # accessible throughout your integration
#     entry.runtime_data = RuntimeData(coordinator)

#     # Setup platforms (based on the list of entity types in PLATFORMS defined above)
#     # This calls the async_setup method in each of your entity type files.
#     await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

#     # Return true to denote a successful setup.
#     return True

# async def async_unload_entry(hass: HomeAssistant, entry: MyConfigEntry) -> bool:
#     """Unload a config entry."""
#     # This is called when you remove your integration or shutdown HA.
#     # If you have created any custom services, they need to be removed here too.
#     LOGGER.warn(f"Polymarket --async_unload_entry-- {entry}")

#     # Unload platforms and return result
#     return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

