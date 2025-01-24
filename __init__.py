"""The fileshare integration."""
import os
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, CONF_BASE_PATH

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up fileshare from a config entry."""
    base_path = entry.data.get(CONF_BASE_PATH, hass.config.path())

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "base_path": base_path
    }

    # Register panel
    if not hass.data[DOMAIN].get("panel_registered"):
        hass.components.frontend.async_register_built_in_panel(
            "fileshare",
            "文件管理器",
            "mdi:folder",
            "panel.html",
            {"admin": True}
        )
        hass.data[DOMAIN]["panel_registered"] = True

    # Register services
    async def list_files(call):
        """List files in directory."""
        path = os.path.join(base_path, call.data.get("path", ""))
        if not path.startswith(base_path):
            return {"error": "Access denied"}

        try:
            files = []
            for name in os.listdir(path):
                full_path = os.path.join(path, name)
                files.append({
                    "name": name,
                    "path": full_path,
                    "is_dir": os.path.isdir(full_path)
                })
            return {"files": files}
        except Exception as e:
            _LOGGER.error(f"Error listing files: {e}")
            return {"error": str(e)}

    async def upload_file(call):
        """Upload file."""
        path = os.path.join(base_path, call.data["path"])
        if not path.startswith(base_path):
            return {"error": "Access denied"}

        try:
            with open(path, "w") as f:
                f.write(call.data["content"])
            return {"success": True}
        except Exception as e:
            _LOGGER.error(f"Error uploading file: {e}")
            return {"error": str(e)}

    async def delete_file(call):
        """Delete file or directory."""
        path = os.path.join(base_path, call.data["path"])
        if not path.startswith(base_path):
            return {"error": "Access denied"}

        try:
            if os.path.isdir(path):
                os.rmdir(path)
            else:
                os.remove(path)
            return {"success": True}
        except Exception as e:
            _LOGGER.error(f"Error deleting file: {e}")
            return {"error": str(e)}

    async def create_directory(call):
        """Create directory."""
        path = os.path.join(base_path, call.data["path"])
        if not path.startswith(base_path):
            return {"error": "Access denied"}

        try:
            os.makedirs(path, exist_ok=True)
            return {"success": True}
        except Exception as e:
            _LOGGER.error(f"Error creating directory: {e}")
            return {"error": str(e)}

    hass.services.async_register(DOMAIN, "list_files", list_files)
    hass.services.async_register(DOMAIN, "upload_file", upload_file)
    hass.services.async_register(DOMAIN, "delete_file", delete_file)
    hass.services.async_register(DOMAIN, "create_directory", create_directory)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
