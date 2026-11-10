"""Set up a point (the home zone by default), a radius and the services; change them later with Configure."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_LATITUDE, CONF_LOCATION, CONF_LONGITUDE
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    LocationSelector,
    LocationSelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import CONF_DIENSTEN, CONF_RADIUS, DIENSTEN, DOMAIN, RADII


def _schema(lat: float, lon: float, radius: str, diensten: list[str]) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(CONF_LOCATION, default={CONF_LATITUDE: lat, CONF_LONGITUDE: lon}): LocationSelector(
                LocationSelectorConfig(radius=False)
            ),
            vol.Required(CONF_RADIUS, default=radius): SelectSelector(
                SelectSelectorConfig(options=RADII, mode=SelectSelectorMode.LIST, translation_key="radius")
            ),
            vol.Required(CONF_DIENSTEN, default=diensten): SelectSelector(
                SelectSelectorConfig(options=DIENSTEN, multiple=True, translation_key="diensten")
            ),
        }
    )


def _check(user_input: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str]]:
    """The entry data from the form, or the errors."""
    lat = user_input[CONF_LOCATION][CONF_LATITUDE]
    lon = user_input[CONF_LOCATION][CONF_LONGITUDE]
    if not (50.7 < lat < 53.7 and 3.2 < lon < 7.3):
        return {}, {CONF_LOCATION: "outside_nl"}
    if not user_input[CONF_DIENSTEN]:
        return {}, {CONF_DIENSTEN: "no_services"}
    data = {CONF_LATITUDE: lat, CONF_LONGITUDE: lon, CONF_RADIUS: user_input[CONF_RADIUS], CONF_DIENSTEN: user_input[CONF_DIENSTEN]}
    return data, {}


def _title(data: dict[str, Any]) -> str:
    return f"P2000 binnen {data[CONF_RADIUS]} km"


class ActueelalarmFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return ActueelalarmOptions()

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            data, errors = _check(user_input)
            if data:
                await self.async_set_unique_id(f"{data[CONF_LATITUDE]:.3f}_{data[CONF_LONGITUDE]:.3f}_{data[CONF_RADIUS]}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=_title(data), data=data)
        schema = _schema(self.hass.config.latitude, self.hass.config.longitude, "5", DIENSTEN)
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)


class ActueelalarmOptions(OptionsFlow):
    """Configure: a new point, radius or services. The entry reloads with them (the update listener in __init__)."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            data, errors = _check(user_input)
            if data:
                # title and options in one update, so the entry reloads once
                self.hass.config_entries.async_update_entry(self.config_entry, title=_title(data), options=data)
                return self.async_create_entry(data=data)
        cur = {**self.config_entry.data, **self.config_entry.options}
        schema = _schema(cur[CONF_LATITUDE], cur[CONF_LONGITUDE], cur[CONF_RADIUS], cur[CONF_DIENSTEN])
        return self.async_show_form(step_id="init", data_schema=schema, errors=errors)
