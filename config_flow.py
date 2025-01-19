"""Config flow for the File Share integration."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, DEFAULT_SHARE_PATH, DEFAULT_PERMISSIONS

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for File Share."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            # Validate share path
            try:
                path = Path(user_input["share_path"])
                if not path.exists():
                    path.mkdir(parents=True)
                return self.async_create_entry(
                    title="File Share",
                    data=user_input
                )
            except Exception as err:
                errors["base"] = "invalid_path"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(
                    "share_path",
                    default=DEFAULT_SHARE_PATH
                ): str,
                vol.Required(
                    "read_permission",
                    default=DEFAULT_PERMISSIONS["read"]
                ): bool,
                vol.Required(
                    "write_permission",
                    default=DEFAULT_PERMISSIONS["write"]
                ): bool,
                vol.Required(
                    "delete_permission",
                    default=DEFAULT_PERMISSIONS["delete"]
                ): bool,
            }),
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for File Share."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Manage the options."""
        errors = {}
        
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    "share_path",
                    default=self.config_entry.data.get("share_path", DEFAULT_SHARE_PATH)
                ): str,
                vol.Required(
                    "read_permission",
                    default=self.config_entry.data.get("read_permission", True)
                ): bool,
                vol.Required(
                    "write_permission",
                    default=self.config_entry.data.get("write_permission", True)
                ): bool,
                vol.Required(
                    "delete_permission",
                    default=self.config_entry.data.get("delete_permission", True)
                ): bool,
            }),
            errors=errors
        )
