import os
import shutil
from pathlib import Path
from typing import List, Dict, Union

class FileManager:
    """Handle file operations for the File Share integration."""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        
    def list_files(self, path: str) -> List[Dict[str, Union[str, bool]]]:
        """List files and directories in a given path."""
        full_path = self.base_path / path.lstrip('/')
        if not full_path.exists():
            raise FileNotFoundError(f"Path {path} does not exist")
            
        result = []
        for item in full_path.iterdir():
            result.append({
                'name': item.name,
                'path': str(item.relative_to(self.base_path)),
                'is_dir': item.is_dir(),
                'size': item.stat().st_size if item.is_file() else 0,
                'modified': item.stat().st_mtime
            })
        return result
        
    def upload_file(self, path: str, content: str) -> None:
        """Upload/create a file with given content."""
        full_path = self.base_path / path.lstrip('/')
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
            
    def download_file(self, path: str) -> str:
        """Download file content."""
        full_path = self.base_path / path.lstrip('/')
        if not full_path.is_file():
            raise FileNotFoundError(f"File {path} does not exist")
        with open(full_path, 'r') as f:
            return f.read()
            
    def delete_file(self, path: str) -> None:
        """Delete a file or directory."""
        full_path = self.base_path / path.lstrip('/')
        if not full_path.exists():
            raise FileNotFoundError(f"Path {path} does not exist")
            
        if full_path.is_file():
            full_path.unlink()
        else:
            shutil.rmtree(full_path)
            
    def create_directory(self, path: str) -> None:
        """Create a new directory."""
        full_path = self.base_path / path.lstrip('/')
        full_path.mkdir(parents=True, exist_ok=True)
