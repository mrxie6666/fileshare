"""The fileshare integration."""
from __future__ import annotations

import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN
from .file_manager import FileManager

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the fileshare component."""
    hass.data.setdefault(DOMAIN, {})
    
    # Register services
    async def handle_list_files(call):
        """Handle list files service."""
        file_manager = hass.data[DOMAIN]["file_manager"]
        path = call.data.get("path")
        try:
            files = await hass.async_add_executor_job(
                file_manager.list_files, path
            )
            return {"files": files}
        except Exception as err:
            _LOGGER.error("Error listing files: %s", err)
            raise

    async def handle_upload_file(call):
        """Handle upload file service."""
        file_manager = hass.data[DOMAIN]["file_manager"]
        path = call.data.get("path")
        content = call.data.get("content")
        try:
            await hass.async_add_executor_job(
                file_manager.upload_file, path, content
            )
        except Exception as err:
            _LOGGER.error("Error uploading file: %s", err)
            raise

    async def handle_download_file(call):
        """Handle download file service."""
        file_manager = hass.data[DOMAIN]["file_manager"]
        path = call.data.get("path")
        try:
            content = await hass.async_add_executor_job(
                file_manager.download_file, path
            )
            return {"content": content}
        except Exception as err:
            _LOGGER.error("Error downloading file: %s", err)
            raise

    async def handle_delete_file(call):
        """Handle delete file service."""
        file_manager = hass.data[DOMAIN]["file_manager"]
        path = call.data.get("path")
        try:
            await hass.async_add_executor_job(
                file_manager.delete_file, path
            )
        except Exception as err:
            _LOGGER.error("Error deleting file: %s", err)
            raise

    hass.services.async_register(DOMAIN, "list_files", handle_list_files)
    hass.services.async_register(DOMAIN, "upload_file", handle_upload_file)
    hass.services.async_register(DOMAIN, "download_file", handle_download_file)
    hass.services.async_register(DOMAIN, "delete_file", handle_delete_file)

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry."""
    config = entry.data
    file_manager = FileManager(config["share_path"])
    file_manager.permissions = {
        "read": config["read_permission"],
        "write": config["write_permission"],
        "delete": config["delete_permission"]
    }
    
    hass.data[DOMAIN]["file_manager"] = file_manager
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data[DOMAIN].pop("file_manager", None)
    return True
