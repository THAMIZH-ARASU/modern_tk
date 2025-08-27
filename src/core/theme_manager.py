"""
Theme Manager - Global theme management and style resolution
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

class ThemeManager:
    """Manages global themes and style resolution"""
    
    def __init__(self):
        self.themes = {}
        self.current_theme = None
        self.global_overrides = {}
        self.color_cache = {}
        
        # Load default themes
        self._load_default_themes()
    
    def _load_default_themes(self):
        """Load built-in themes"""
        # Default Light Theme
        self.register_theme('default', {
            'name': 'Default Light',
            'colors': {
                'primary': '#007ACC',
                'secondary': '#6C757D', 
                'success': '#28A745',
                'warning': '#FFC107',
                'danger': '#DC3545',
                'background': '#FFFFFF',
                'surface': '#F8F9FA',
                'text': '#212529',
                'text_secondary': '#6C757D',
                'border': '#DEE2E6'
            },
            'widgets': {
                'button': {
                    'bg': 'primary',
                    'fg': 'white',
                    'font': ('Segoe UI', 10),
                    'padding': (12, 8),
                    'radius': 4,
                    'hover_bg': '#0056b3',
                    'active_bg': '#004085'
                },
                'frame': {
                    'bg': 'background',
                    'relief': 'flat'
                },
                'label': {
                    'bg': 'background',
                    'fg': 'text',
                    'font': ('Segoe UI', 10)
                },
                'entry': {
                    'bg': 'white',
                    'fg': 'text',
                    'font': ('Segoe UI', 10),
                    'relief': 'solid',
                    'borderwidth': 1,
                    'radius': 4,
                    'focus_bg': '#fff',
                    'focus_border': 'primary'
                }
            }
        })
        
        # Dark Theme
        self.register_theme('dark', {
            'name': 'Dark Mode',
            'colors': {
                'primary': '#0D6EFD',
                'secondary': '#6C757D',
                'success': '#198754',
                'warning': '#FFC107',
                'danger': '#DC3545',
                'background': '#212529',
                'surface': '#343A40',
                'text': '#F8F9FA',
                'text_secondary': '#ADB5BD',
                'border': '#495057'
            },
            'widgets': {
                'button': {
                    'bg': 'primary',
                    'fg': 'white',
                    'font': ('Segoe UI', 10),
                    'padding': (12, 8),
                    'radius': 4,
                    'hover_bg': '#0B5ED7',
                    'active_bg': '#0A58CA'
                },
                'frame': {
                    'bg': 'background',
                    'relief': 'flat'
                },
                'label': {
                    'bg': 'background',
                    'fg': 'text',
                    'font': ('Segoe UI', 10)
                },
                'entry': {
                    'bg': 'surface',
                    'fg': 'text',
                    'font': ('Segoe UI', 10),
                    'relief': 'solid',
                    'borderwidth': 1,
                    'radius': 4,
                    'focus_bg': 'surface',
                    'focus_border': 'primary'
                }
            }
        })
        
        # Set default theme
        self.use('default')
    
    def register_theme(self, name: str, theme_dict: Dict[str, Any]):
        """Register a new theme"""
        self.themes[name] = theme_dict
    
    def use(self, theme_name: str):
        """Switch to a specific theme"""
        if theme_name not in self.themes:
            raise ValueError(f"Theme '{theme_name}' not found")
        
        self.current_theme = theme_name
        self.color_cache.clear()  # Clear color cache when switching themes
    
    def get_current_theme(self) -> Optional[Dict[str, Any]]:
        """Get the currently active theme"""
        return self.themes.get(self.current_theme) if self.current_theme else None
    
    def get_widget_style(self, widget_type: str) -> Dict[str, Any]:
        """Get style for a specific widget type from current theme"""
        theme = self.get_current_theme()
        if not theme:
            return {}
        
        widgets = theme.get('widgets', {})
        return widgets.get(widget_type, {}).copy()
    
    def resolve_color(self, color_ref: str) -> str:
        """Resolve color reference to actual color value"""
        # Check cache first
        cache_key = f"{self.current_theme}:{color_ref}"
        if cache_key in self.color_cache:
            return self.color_cache[cache_key]
        
        theme = self.get_current_theme()
        if not theme:
            return color_ref
        
        colors = theme.get('colors', {})
        resolved = colors.get(color_ref, color_ref)
        
        # Cache the result
        self.color_cache[cache_key] = resolved
        return resolved
    
    def set_global_override(self, property_path: str, value: Any):
        """Set global style override (e.g., 'button.bg', 'colors.primary')"""
        self.global_overrides[property_path] = value
    
    def clear_global_overrides(self):
        """Clear all global overrides"""
        self.global_overrides.clear()
    
    def get_available_themes(self) -> list:
        """Get list of available theme names"""
        return list(self.themes.keys())
    
    def export_theme(self, theme_name: str, filepath: str):
        """Export theme to JSON file"""
        if theme_name not in self.themes:
            raise ValueError(f"Theme '{theme_name}' not found")
        
        theme_data = self.themes[theme_name]
        with open(filepath, 'w') as f:
            json.dump(theme_data, f, indent=2)
    
    def import_theme(self, filepath: str, theme_name: str = None):
        """Import theme from JSON file"""
        with open(filepath, 'r') as f:
            theme_data = json.load(f)
        
        name = theme_name or theme_data.get('name', Path(filepath).stem)
        self.register_theme(name, theme_data)
        return name