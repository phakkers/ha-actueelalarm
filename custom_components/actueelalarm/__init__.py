"""actueelalarm P2000: Dutch emergency alerts (fire, ambulance, trauma helicopter, KNRM) near a point."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API, CONF_DIENSTEN, CONF_RADIUS, DOMAIN, EVENT, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.SENSOR]


class Coordinator(DataUpdateCoordinator[list[dict[str, Any]]]):
    """Polls the open feed every minute and fires an event for every new melding."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL, config_entry=entry)
        self.entry = entry
        # None until the first fetch: what is already there on start-up is not news
        self.seen: set[str] | None = None

    async def _async_update_data(self) -> list[dict[str, Any]]:
        d = self.entry.data
        params = {
            "lat": f"{d[CONF_LATITUDE]:.4f}",
            "lon": f"{d[CONF_LONGITUDE]:.4f}",
            "km": d[CONF_RADIUS],
            "diensten": ",".join(d[CONF_DIENSTEN]),
        }
        try:
            async with async_get_clientsession(self.hass).get(
                API, params=params, timeout=aiohttp.ClientTimeout(total=20)
            ) as res:
                res.raise_for_status()
                data = (await res.json())["meldingen"]
        except (aiohttp.ClientError, TimeoutError, KeyError, ValueError) as err:
            raise UpdateFailed(f"actueelalarm.nl: {err}") from err
        if self.seen is not None:
            for m in reversed(data):  # oldest first
                if m["id"] not in self.seen:
                    self.hass.bus.async_fire(EVENT, {**m, "entry_id": self.entry.entry_id})
        # the feed covers the last 2 hours; a melding that left it never comes back
        self.seen = {m["id"] for m in data}
        return data


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = Coordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
