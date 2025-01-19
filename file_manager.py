"""File manager for the File Share integration."""
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from .const import DEFAULT_SHARE_PATH, DEFAULT_PERMISSIONS

class FileManager:
    """Manage file operations for the File Share integration."""

    def __init__(self, share_path: str = DEFAULT_SHARE_PATH):
        """Initialize the file manager."""
        self.share_path = Path(share_path)
        self.permissions = DEFAULT_PERMISSIONS
        self._ensure_share_directory()

    def _ensure_share_directory(self):
        """Ensure the share directory exists."""
        self.share_path.mkdir(parents=True, exist_ok=True)

    def list_files(self, path: str) -> List[Dict]:
        """List files in a directory."""
        target_path = self.share_path / path.lstrip('/')
        if not target_path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")
            
        return [
            {
                "name": f.name,
                "is_dir": f.is_dir(),
                "size": f.stat().st_size if f.is_file() else 0,
                "modified": f.stat().st_mtime
            }
            for f in target_path.iterdir()
        ]

    def upload_file(self, path: str, content: str) -> None:
        """Upload a file."""
        if not self.permissions["write"]:
            raise PermissionError("Write permission denied")
            
        target_path = self.share_path / path.lstrip('/')
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content)

    def download_file(self, path: str) -> str:
        """Download a file."""
        if not self.permissions["read"]:
            raise PermissionError("Read permission denied")
            
        target_path = self.share_path / path.lstrip('/')
        if not target_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
            
        return target_path.read_text()

    def delete_file(self, path: str) -> None:
        """Delete a file or directory."""
        if not self.permissions["delete"]:
            raise PermissionError("Delete permission denied")
            
        target_path = self.share_path / path.lstrip('/')
        if not target_path.exists():
            raise FileNotFoundError(f"Path not found: {path}")
            
        if target_path.is_dir():
            shutil.rmtree(target_path)
        else:
            target_path.unlink()
