"""Set up a point (the home zone by default), a radius and the services."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_LATITUDE, CONF_LOCATION, CONF_LONGITUDE
from homeassistant.helpers.selector import (
    LocationSelector,
    LocationSelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import CONF_DIENSTEN, CONF_RADIUS, DIENSTEN, DOMAIN, RADII


class ActueelalarmFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            lat = user_input[CONF_LOCATION][CONF_LATITUDE]
            lon = user_input[CONF_LOCATION][CONF_LONGITUDE]
            if not (50.7 < lat < 53.7 and 3.2 < lon < 7.3):
                errors[CONF_LOCATION] = "outside_nl"
            elif not user_input[CONF_DIENSTEN]:
                errors[CONF_DIENSTEN] = "no_services"
            else:
                await self.async_set_unique_id(f"{lat:.3f}_{lon:.3f}_{user_input[CONF_RADIUS]}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"P2000 binnen {user_input[CONF_RADIUS]} km",
                    data={
                        CONF_LATITUDE: lat,
                        CONF_LONGITUDE: lon,
                        CONF_RADIUS: user_input[CONF_RADIUS],
                        CONF_DIENSTEN: user_input[CONF_DIENSTEN],
                    },
                )
        schema = vol.Schema(
            {
                vol.Required(
                    CONF_LOCATION,
                    default={CONF_LATITUDE: self.hass.config.latitude, CONF_LONGITUDE: self.hass.config.longitude},
                ): LocationSelector(LocationSelectorConfig(radius=False)),
                vol.Required(CONF_RADIUS, default="5"): SelectSelector(
                    SelectSelectorConfig(options=RADII, mode=SelectSelectorMode.DROPDOWN, translation_key="radius")
                ),
                vol.Required(CONF_DIENSTEN, default=DIENSTEN): SelectSelector(
                    SelectSelectorConfig(options=DIENSTEN, multiple=True, translation_key="diensten")
                ),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
