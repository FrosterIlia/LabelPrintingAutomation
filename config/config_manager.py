import json
import os
from typing import Dict, Any, Optional

class ConfigManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file or create default config"""
        default_config = {
            "selected_printer": "",
            "button_mappings": {},
            "server_port": 9000,
            "server_host": "0.0.0.0"
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}. Using defaults.")
                return default_config
        else:
            return default_config
    
    def save_config(self) -> bool:
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value
    
    def get_selected_printer(self) -> str:
        """Get currently selected printer name"""
        return self.config.get("selected_printer", "")
    
    def set_selected_printer(self, printer_name: str) -> None:
        """Set selected printer"""
        self.config["selected_printer"] = printer_name
    
    def get_button_mappings(self) -> Dict[str, str]:
        """Get button ID to label file mappings"""
        return self.config.get("button_mappings", {})
    
    def set_button_mappings(self, mappings: Dict[str, str]) -> None:
        """Set button ID to label file mappings"""
        self.config["button_mappings"] = mappings
    
    def add_button_mapping(self, button_id: str, label_file: str) -> None:
        """Add a single button mapping"""
        if "button_mappings" not in self.config:
            self.config["button_mappings"] = {}
        self.config["button_mappings"][button_id] = label_file
    
    def remove_button_mapping(self, button_id: str) -> None:
        """Remove a button mapping"""
        if "button_mappings" in self.config and button_id in self.config["button_mappings"]:
            del self.config["button_mappings"][button_id]
    
    def get_server_config(self) -> tuple[str, int]:
        """Get server host and port"""
        return (
            self.config.get("server_host", "0.0.0.0"),
            self.config.get("server_port", 5000)
        )
