"""
Modern Tkinter UI Library

A modern, CSS-inspired styling system for Tkinter applications.
Provides declarative styling, theming, and enhanced widgets.
"""

__version__ = "0.1.0"

# Core imports
from .core.theme_manager import ThemeManager
from .core.style_engine import StyleEngine

# Widget imports
from .widgets.button import Button
from .widgets.frame import Frame
from .widgets.label import Label
from .widgets.entry import Entry
from .widgets.text import Text
from .widgets.checkbox import Checkbox
from .widgets.radiobutton import RadioButton
from .widgets.progressbar import ProgressBar

# Layout imports

# Theme imports
from .themes import default_theme, dark_theme, material_theme, fluent_theme

# Utility classes
from .utils.colors import Color
from .utils.fonts import FontManager

# Main application class
import tkinter as tk
from typing import Optional, Dict, Any

class App:
    """Main application class with theme support"""
    
    def __init__(self, theme: str = "default", **kwargs):
        self.root = tk.Tk()
        self.theme_manager = ThemeManager()
        self.style_engine = StyleEngine(self.theme_manager)
        
        # Set theme
        if theme == "default":
            self.theme_manager.set_theme(default_theme)
        elif theme == "dark":
            self.theme_manager.set_theme(dark_theme)
        elif theme == "material":
            self.theme_manager.set_theme(material_theme)
        elif theme == "fluent":
            self.theme_manager.set_theme(fluent_theme)
        
        # Configure root window
        for key, value in kwargs.items():
            if hasattr(self.root, key):
                setattr(self.root, key, value)
    
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()
    
    def __getattr__(self, name):
        """Delegate to root window"""
        return getattr(self.root, name)

# Style class decorator
def StyleClass(cls):
    """Decorator to create reusable style classes"""
    cls._is_style_class = True
    return cls

# Global theme manager instance
_global_theme_manager = ThemeManager()

class Theme:
    """Global theme management interface"""
    
    @staticmethod
    def register(name: str, theme_dict: Dict[str, Any]):
        """Register a new theme"""
        _global_theme_manager.register_theme(name, theme_dict)
    
    @staticmethod
    def use(name: str):
        """Set the active theme"""
        _global_theme_manager.use_theme(name)
    
    @staticmethod
    def get(key: str):
        """Get a theme value"""
        return _global_theme_manager.get_theme_value(key)

__all__ = [
    # Core classes
    'App', 'Theme', 'StyleClass',
    
    # Widgets
    'Button', 'Frame', 'Label', 'Entry', 'Text',
    'Checkbox', 'RadioButton', 'ProgressBar',
    
    # Layouts
    'Container', 'FlexLayout', 'ResponsiveGrid',
    
    # Themes
    'default_theme', 'dark_theme', 'material_theme', 'fluent_theme',
    
    # Utils
    'Color', 'FontManager'
]