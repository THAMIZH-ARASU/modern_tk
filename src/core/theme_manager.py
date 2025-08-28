"""
Global theme management system for Modern TK.
Handles theme loading, switching, and value resolution.
"""

from typing import Dict, Any, Optional
import json
import os

class ThemeManager:
    """Global theme management system"""
    
    def __init__(self):
        self.themes = {}
        self.current_theme = None
        self.theme_stack = []
    
    def register_theme(self, name: str, theme_dict: Dict[str, Any]):
        """Register a new theme"""
        self.themes[name] = theme_dict
    
    def set_theme(self, theme: Dict[str, Any]):
        """Set the current theme"""
        self.current_theme = theme
    
    def use_theme(self, name: str):
        """Switch to a registered theme by name"""
        if name in self.themes:
            self.current_theme = self.themes[name]
        else:
            raise ValueError(f"Theme '{name}' not found")
    
    def push_theme(self, theme: Dict[str, Any]):
        """Push a theme onto the stack"""
        if self.current_theme:
            self.theme_stack.append(self.current_theme)
        self.current_theme = theme
    
    def pop_theme(self):
        """Pop the last theme from the stack"""
        if self.theme_stack:
            self.current_theme = self.theme_stack.pop()
        else:
            self.current_theme = None
    
    def get_theme_value(self, key: str, default=None) -> Any:
        """Get a value from the current theme using dot notation"""
        if not self.current_theme:
            return default
        
        keys = key.split('.')
        value = self.current_theme
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_widget_theme(self, widget_type: str) -> Dict[str, Any]:
        """Get theme settings for a specific widget type"""
        return self.get_theme_value(f"widgets.{widget_type}", {})
    
    def get_color(self, color_name: str) -> str:
        """Get a color from the theme's color palette"""
        return self.get_theme_value(f"colors.{color_name}", color_name)
    
    def get_font(self, font_name: str) -> tuple:
        """Get a font from the theme's font definitions"""
        return self.get_theme_value(f"fonts.{font_name}", ('TkDefaultFont', 10, 'normal'))
    
    def load_theme_from_file(self, filepath: str) -> Dict[str, Any]:
        """Load a theme from a JSON file"""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def save_theme_to_file(self, theme_dict: Dict[str, Any], filepath: str):
        """Save a theme to a JSON file"""
        with open(filepath, 'w') as f:
            json.dump(theme_dict, f, indent=2)
    
    def merge_themes(self, base_theme: Dict[str, Any], overlay_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two themes, with overlay taking precedence"""
        result = base_theme.copy()
        
        def deep_merge(base_dict, overlay_dict):
            for key, value in overlay_dict.items():
                if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                    base_dict[key] = deep_merge(base_dict[key], value)
                else:
                    base_dict[key] = value
            return base_dict
        
        return deep_merge(result, overlay_theme)
    
    def create_variant(self, base_theme: str, modifications: Dict[str, Any], variant_name: str):
        """Create a theme variant with modifications"""
        if base_theme not in self.themes:
            raise ValueError(f"Base theme '{base_theme}' not found")
        
        base = self.themes[base_theme]
        variant = self.merge_themes(base, modifications)
        self.register_theme(variant_name, variant)
        return variant