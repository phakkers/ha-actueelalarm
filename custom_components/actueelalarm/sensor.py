"""The latest melding near the configured point, with its place on the map."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import Coordinator
from .const import ATTRIBUTION, DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, add: AddEntitiesCallback) -> None:
    add([LaatsteMelding(entry.runtime_data)])


class LaatsteMelding(CoordinatorEntity[Coordinator], SensorEntity):
    """State: the latest melding's title. Attributes: service, priority, place, street, distance, link, position."""

    _attr_has_entity_name = True
    _attr_translation_key = "laatste_melding"
    _attr_icon = "mdi:alarm-light"
    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: Coordinator) -> None:
        super().__init__(coordinator)
        entry = coordinator.entry
        self._attr_unique_id = f"{entry.entry_id}_laatste_melding"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="actueelalarm.nl",
            entry_type=DeviceEntryType.SERVICE,
            configuration_url="https://actueelalarm.nl/",
        )

    @property
    def _melding(self) -> dict[str, Any] | None:
        return self.coordinator.data[0] if self.coordinator.data else None

    @property
    def native_value(self) -> str | None:
        m = self._melding
        return m["titel"][:255] if m else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        m = self._melding
        attrs: dict[str, Any] = {"aantal_laatste_2_uur": len(self.coordinator.data or [])}
        if m:
            attrs |= {
                "dienst": m["dienst_naam"],
                "prio": m["prio_naam"],
                "plaats": m["plaats"],
                "straat": m["straat"],
                "afstand_km": m["km"],
                "tijd": m["t"],
                "url": m["url"],
                "latitude": m["lat"],
                "longitude": m["lon"],
            }
        return attrs
