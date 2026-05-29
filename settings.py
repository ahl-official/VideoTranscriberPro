"""
Settings module for Video Transcriber Pro.
Manages persistent configuration and API key storage.
"""

import os
import json
import logging
from pathlib import Path


class AppSettings:
    """
    Manages application settings including API key persistence.
    Stores settings in user's home directory under .video_transcriber/
    """
    
    def __init__(self):
        """Initialize settings manager."""
        self.config_dir = Path.home() / ".video_transcriber"
        self.config_file = self.config_dir / "settings.json"
        self._ensure_config_dir()
        self.settings = self._load_settings()
    
    def _ensure_config_dir(self):
        """Create config directory if it doesn't exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_settings(self):
        """Load settings from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_settings(self):
        """Save settings to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except IOError as e:
            logging.error("Error saving settings: %s", e)
    
    def get_api_key(self):
        """
        Get saved API key from settings or environment.
        
        Returns:
            str: API key if found, empty string otherwise
        """
        # First check environment variable
        env_key = os.getenv('ASSEMBLYAI_API_KEY', '')
        if env_key:
            return env_key
        
        # Then check saved settings
        return self.settings.get('api_key', '')
    
    def set_api_key(self, api_key):
        """
        Save API key to settings file.
        
        Args:
            api_key (str): API key to save
        """
        if api_key:
            self.settings['api_key'] = api_key
            self._save_settings()
    
    def has_api_key(self):
        """
        Check if API key exists (saved or in environment).
        
        Returns:
            bool: True if API key is available
        """
        return bool(self.get_api_key())
    
    def clear_api_key(self):
        """Remove saved API key from settings."""
        if 'api_key' in self.settings:
            del self.settings['api_key']
            self._save_settings()
    
    def get_config_path(self):
        """Get path to config directory."""
        return str(self.config_dir)


# Global settings instance
_settings = None


def get_settings():
    """Get global settings instance."""
    global _settings
    if _settings is None:
        _settings = AppSettings()
    return _settings
