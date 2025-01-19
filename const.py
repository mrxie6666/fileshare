"""Constants for the File Share integration."""
from pathlib import Path

DOMAIN = "fileshare"
DEFAULT_SHARE_PATH = str(Path.home() / "shared_files")
DEFAULT_PERMISSIONS = {
    "read": True,
    "write": True,
    "delete": True
}

# Service names
SERVICE_LIST_FILES = "list_files"
SERVICE_UPLOAD_FILE = "upload_file"
SERVICE_DOWNLOAD_FILE = "download_file"
SERVICE_DELETE_FILE = "delete_file"
