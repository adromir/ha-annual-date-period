"""Binary sensor platform for Annual Date Period integration."""
from __future__ import annotations

import calendar
from datetime import date
import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_change
import homeassistant.util.dt as dt_util

from .const import (
    CONF_START_MONTH,
    CONF_START_DAY,
    CONF_END_MONTH,
    CONF_END_DAY,
    CONF_ICON,
    DEFAULT_ICON,
    ATTR_START_DATE,
    ATTR_END_DATE,
    ATTR_SPANS_NEW_YEAR,
    ATTR_DAYS_REMAINING,
    ATTR_DAYS_UNTIL_START,
    ATTR_NEXT_START,
    ATTR_NEXT_END,
)

_LOGGER = logging.getLogger(__name__)


def safe_date(year: int, month: int, day: int) -> date:
    """Create a date object safely handling leap years."""
    max_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(day, max_day))


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Annual Date Period binary sensor."""
    async_add_entities([AnnualDatePeriodBinarySensor(entry)], True)


class AnnualDatePeriodBinarySensor(BinarySensorEntity):
    """Representation of an Annual Date Period binary sensor."""

    _attr_has_entity_name = True
    _attr_translation_key = "annual_date_period"
    _attr_should_poll = False

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self.entry = entry
        self._attr_unique_id = f"annual_date_period_{entry.entry_id}"
        custom_name = entry.data.get(CONF_NAME)
        if custom_name and custom_name not in ("Heizperiode", "Annual Date Period", "Periode Tanggal Tahunan"):
            self._attr_name = custom_name
        else:
            self._attr_name = None
        self._is_on = False
        self._attrs: dict[str, Any] = {}

    @property
    def is_on(self) -> bool:
        """Return True if today is within the configured period."""
        return self._is_on

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        data = {**self.entry.data, **self.entry.options}
        return data.get(CONF_ICON, DEFAULT_ICON)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the extra state attributes."""
        return self._attrs

    async def async_added_to_hass(self) -> None:
        """Register midnight update listener when entity is added."""
        self._calculate_state()

        @callback
        def _async_midnight_update(*_: Any) -> None:
            """Recalculate state when date changes at midnight."""
            self._calculate_state()
            self.async_write_ha_state()

        self.async_on_remove(
            async_track_time_change(
                self.hass, _async_midnight_update, hour=0, minute=0, second=0
            )
        )

    def _calculate_state(self) -> None:
        """Calculate is_on and all attributes based on current date."""
        data = {**self.entry.data, **self.entry.options}
        start_month = int(data.get(CONF_START_MONTH, 10))
        start_day = int(data.get(CONF_START_DAY, 15))
        end_month = int(data.get(CONF_END_MONTH, 4))
        end_day = int(data.get(CONF_END_DAY, 15))

        today = dt_util.now().date()
        today_tuple = (today.month, today.day)
        start_tuple = (start_month, start_day)
        end_tuple = (end_month, end_day)

        spans_new_year = start_tuple > end_tuple

        if spans_new_year:
            is_active = (today_tuple >= start_tuple) or (today_tuple <= end_tuple)
            # Next start
            if today_tuple >= start_tuple:
                next_start = safe_date(today.year + 1, start_month, start_day)
            elif today_tuple <= end_tuple:
                next_start = safe_date(today.year, start_month, start_day)
            else:
                next_start = safe_date(today.year, start_month, start_day)

            # Next end
            if today_tuple >= start_tuple:
                next_end = safe_date(today.year + 1, end_month, end_day)
            elif today_tuple <= end_tuple:
                next_end = safe_date(today.year, end_month, end_day)
            else:
                next_end = safe_date(today.year + 1, end_month, end_day)
        else:
            is_active = start_tuple <= today_tuple <= end_tuple

            # Next start
            if today_tuple <= start_tuple:
                next_start = safe_date(today.year, start_month, start_day)
            else:
                next_start = safe_date(today.year + 1, start_month, start_day)

            # Next end
            if is_active or today_tuple <= end_tuple:
                next_end = safe_date(today.year, end_month, end_day)
            else:
                next_end = safe_date(today.year + 1, end_month, end_day)

        days_remaining = (next_end - today).days if is_active else None
        days_until_start = (next_start - today).days if not is_active else None

        self._is_on = is_active
        self._attrs = {
            ATTR_START_DATE: f"{start_day:02d}.{start_month:02d}.",
            ATTR_END_DATE: f"{end_day:02d}.{end_month:02d}.",
            ATTR_SPANS_NEW_YEAR: spans_new_year,
            ATTR_DAYS_REMAINING: days_remaining,
            ATTR_DAYS_UNTIL_START: days_until_start,
            ATTR_NEXT_START: next_start.isoformat(),
            ATTR_NEXT_END: next_end.isoformat(),
        }
