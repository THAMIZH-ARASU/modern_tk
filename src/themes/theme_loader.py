"""Theme loading utilities for Modern TK"""

import json
import os
from typing import Dict, Any, Optional

class ThemeLoader:
    """Loads themes from various sources"""
    
    @staticmethod
    def load_from_file(file_path: str) -> Optional[Dict[str, Any]]:
        """Load a theme from a JSON file"""
        try:
            with open(file_path, 'r') as f:
                theme_data = json.load(f)
            return theme_data
        except Exception as e:
            print(f"Error loading theme from {file_path}: {e}")
            return None
    
    @staticmethod
    def load_from_string(json_string: str) -> Optional[Dict[str, Any]]:
        """Load a theme from a JSON string"""
        try:
            theme_data = json.loads(json_string)
            return theme_data
        except Exception as e:
            print(f"Error parsing theme JSON: {e}")
            return None
    
    @staticmethod
    def save_to_file(theme_data: Dict[str, Any], file_path: str) -> bool:
        """Save a theme to a JSON file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w') as f:
                json.dump(theme_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving theme to {file_path}: {e}")
            return False
    
    @staticmethod
    def merge_themes(base_theme: Dict[str, Any], override_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two themes, with override_theme taking precedence"""
        merged = base_theme.copy()
        
        # Merge top-level keys
        for key, value in override_theme.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                # Recursively merge dictionaries
                merged[key] = ThemeLoader.merge_themes(merged[key], value)
            else:
                # Override or add new value
                merged[key] = value
        
        return merged
    
    @staticmethod
    def validate_theme(theme_data: Dict[str, Any]) -> bool:
        """Validate theme structure"""
        required_keys = ['name', 'version']
        for key in required_keys:
            if key not in theme_data:
                print(f"Theme validation failed: Missing required key '{key}'")
                return False
        
        # Check for colors section
        if 'colors' not in theme_data or not isinstance(theme_data['colors'], dict):
            print("Theme validation failed: Invalid or missing 'colors' section")
            return False
        
        # Check for fonts section
        if 'fonts' not in theme_data or not isinstance(theme_data['fonts'], dict):
            print("Theme validation failed: Invalid or missing 'fonts' section")
            return False
        
        return True
    
    @staticmethod
    def get_theme_info(theme_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get basic information about a theme"""
        return {
            'name': theme_data.get('name', 'Unknown'),
            'version': theme_data.get('version', '1.0'),
            'description': theme_data.get('description', ''),
            'author': theme_data.get('author', 'Unknown')
        }