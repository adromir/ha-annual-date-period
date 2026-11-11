"""Config flow for Annual Date Period integration."""
from __future__ import annotations

import logging
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_START_MONTH,
    CONF_START_DAY,
    CONF_END_MONTH,
    CONF_END_DAY,
    CONF_ICON,
    DEFAULT_ICON,
)

_LOGGER = logging.getLogger(__name__)

MONTH_OPTIONS = [
    {"value": "1", "label": "01 - January"},
    {"value": "2", "label": "02 - February"},
    {"value": "3", "label": "03 - March"},
    {"value": "4", "label": "04 - April"},
    {"value": "5", "label": "05 - May"},
    {"value": "6", "label": "06 - June"},
    {"value": "7", "label": "07 - July"},
    {"value": "8", "label": "08 - August"},
    {"value": "9", "label": "09 - September"},
    {"value": "10", "label": "10 - October"},
    {"value": "11", "label": "11 - November"},
    {"value": "12", "label": "12 - December"},
]

MAX_DAYS_PER_MONTH = {
    1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
}


def _validate_date(month: int, day: int) -> bool:
    """Check if day is valid for the given month."""
    if month < 1 or month > 12:
        return False
    max_days = MAX_DAYS_PER_MONTH.get(month, 31)
    return 1 <= day <= max_days


class AnnualDatePeriodConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Annual Date Period."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            start_month = int(user_input[CONF_START_MONTH])
            start_day = int(user_input[CONF_START_DAY])
            end_month = int(user_input[CONF_END_MONTH])
            end_day = int(user_input[CONF_END_DAY])

            if not _validate_date(start_month, start_day):
                errors["base"] = "invalid_start_date"
            elif not _validate_date(end_month, end_day):
                errors["base"] = "invalid_end_date"
            else:
                data = {
                    CONF_NAME: user_input[CONF_NAME],
                    CONF_START_MONTH: start_month,
                    CONF_START_DAY: start_day,
                    CONF_END_MONTH: end_month,
                    CONF_END_DAY: end_day,
                    CONF_ICON: user_input.get(CONF_ICON, DEFAULT_ICON),
                }
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=data,
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default="Heizperiode"): selector.TextSelector(),
                vol.Required(
                    CONF_START_MONTH, default="10"
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=MONTH_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="months",
                    )
                ),
                vol.Required(
                    CONF_START_DAY, default=15
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1,
                        max=31,
                        step=1,
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Required(
                    CONF_END_MONTH, default="4"
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=MONTH_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="months",
                    )
                ),
                vol.Required(
                    CONF_END_DAY, default=15
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1,
                        max=31,
                        step=1,
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(
                    CONF_ICON, default=DEFAULT_ICON
                ): selector.IconSelector(),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return AnnualDatePeriodOptionsFlowHandler(config_entry)


class AnnualDatePeriodOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Annual Date Period."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}

        current_data = {**self.config_entry.data, **self.config_entry.options}

        if user_input is not None:
            start_month = int(user_input[CONF_START_MONTH])
            start_day = int(user_input[CONF_START_DAY])
            end_month = int(user_input[CONF_END_MONTH])
            end_day = int(user_input[CONF_END_DAY])

            if not _validate_date(start_month, start_day):
                errors["base"] = "invalid_start_date"
            elif not _validate_date(end_month, end_day):
                errors["base"] = "invalid_end_date"
            else:
                return self.async_create_entry(
                    title="",
                    data={
                        CONF_START_MONTH: start_month,
                        CONF_START_DAY: start_day,
                        CONF_END_MONTH: end_month,
                        CONF_END_DAY: end_day,
                        CONF_ICON: user_input.get(
                            CONF_ICON, current_data.get(CONF_ICON, DEFAULT_ICON)
                        ),
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_START_MONTH,
                    default=str(current_data.get(CONF_START_MONTH, 10)),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=MONTH_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="months",
                    )
                ),
                vol.Required(
                    CONF_START_DAY,
                    default=int(current_data.get(CONF_START_DAY, 15)),
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1,
                        max=31,
                        step=1,
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Required(
                    CONF_END_MONTH,
                    default=str(current_data.get(CONF_END_MONTH, 4)),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=MONTH_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        translation_key="months",
                    )
                ),
                vol.Required(
                    CONF_END_DAY,
                    default=int(current_data.get(CONF_END_DAY, 15)),
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1,
                        max=31,
                        step=1,
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Optional(
                    CONF_ICON,
                    default=current_data.get(CONF_ICON, DEFAULT_ICON),
                ): selector.IconSelector(),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            errors=errors,
        )
