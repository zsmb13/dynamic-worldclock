"""Support for showing the time in a different time zone."""
from __future__ import annotations

from datetime import tzinfo

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_NAME, CONF_TIME_ZONE, CONF_VALUE_TEMPLATE
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.template import Template
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import homeassistant.util.dt as dt_util

CONF_TIME_FORMAT = "time_format"

DEFAULT_NAME = "Worldclock Sensor"
DEFAULT_TIME_STR_FORMAT = "%H:%M"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        # vol.Required(CONF_TIME_ZONE): cv.time_zone,
        # CONF_NAME: Template(device_config.get(CONF_NAME, object_id), hass),
        vol.Required(CONF_TIME_ZONE): cv.template,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_TIME_FORMAT, default=DEFAULT_TIME_STR_FORMAT): cv.string,
    }
)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the World clock sensor."""
    time_zone_template: Template = config.get(CONF_TIME_ZONE)
    async_add_entities(
        [
            WorldClockSensor(
                time_zone_template,
                config[CONF_NAME],
                config[CONF_TIME_FORMAT],
            )
        ],
        True,
    )


class WorldClockSensor(SensorEntity):
    """Representation of a World clock sensor."""

    _attr_icon = "mdi:clock"

    def __init__(self, time_zone_template: Template, name: str, time_format: str) -> None:
        """Initialize the sensor."""
        self._attr_name = name
        self._time_zone_template = time_zone_template
        self._time_format = time_format

    async def async_update(self) -> None:
        """Get the time and updates the states."""
        # if self._value_template:
        #     value = self._value_template.async_render_with_possible_json_value(
        #         payload, None
        #     )
        tz = dt_util.get_time_zone(self._time_zone_template.async_render_with_possible_json_value(None, None))
        self._attr_native_value = dt_util.now(time_zone=tz).strftime(
            self._time_format
        )
