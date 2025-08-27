"""
Modern Tkinter UI Library
A Pythonic, declarative UI library built on top of Tkinter
"""

import tkinter as tk
from typing import Dict, Any, Optional

# Core components
from src.core.style_engine import StyleEngine
from src.core.theme_manager import ThemeManager
from src.core.style_resolver import StyleResolver

# Widgets
from .widgets.button import Button

# Global instances
_style_engine = StyleEngine()
_theme_manager = ThemeManager()
_style_resolver = StyleResolver(_theme_manager)

# Inject dependencies
_style_engine.theme_manager = _theme_manager

class App:
    """Main application class - simplified Tkinter app with theme support"""
    
    def __init__(self, title="Modern Tkinter App", size=(800, 600), 
                 theme="default", **kwargs):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{size[0]}x{size[1]}")
        
        # Apply theme
        Theme.use(theme)
        
        # Configure root styling
        if theme == 'dark':
            self.root.config(bg='#212529')
        else:
            self.root.config(bg='#FFFFFF')
        
        # Apply any additional kwargs to root
        if kwargs:
            self.root.config(**kwargs)
    
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()
    
    def quit(self):
        """Quit the application"""
        self.root.quit()

class Theme:
    """Static interface for theme management"""
    
    @staticmethod
    def use(theme_name: str):
        """Switch to a specific theme"""
        _theme_manager.use(theme_name)
    
    @staticmethod
    def register(name: str, theme_dict: Dict[str, Any]):
        """Register a new theme"""
        _theme_manager.register_theme(name, theme_dict)
    
    @staticmethod
    def current() -> Optional[str]:
        """Get current theme name"""
        return _theme_manager.current_theme
    
    @staticmethod
    def available() -> list:
        """Get list of available themes"""
        return _theme_manager.get_available_themes()
    
    @staticmethod
    def export(theme_name: str, filepath: str):
        """Export theme to file"""
        _theme_manager.export_theme(theme_name, filepath)
    
    @staticmethod
    def import_theme(filepath: str, name: str = None) -> str:
        """Import theme from file"""
        return _theme_manager.import_theme(filepath, name)

class StyleClass:
    """Decorator for creating reusable style classes"""
    
    def __init__(self, cls):
        self.cls = cls
        self._style_dict = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert style class to dictionary"""
        if self._style_dict is None:
            self._style_dict = {}
            for attr in dir(self.cls):
                if not attr.startswith('_'):
                    value = getattr(self.cls, attr)
                    if not callable(value):
                        self._style_dict[attr] = value
        return self._style_dict.copy()

# Inject global dependencies into widgets
def _inject_dependencies():
    """Inject global dependencies into all widgets"""
    from .core.base_widget import BaseWidget
    
    # Patch BaseWidget to include global dependencies
    original_init = BaseWidget.__init__
    
    def patched_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        self.style_engine = _style_engine
        self.theme_manager = _theme_manager
        
        # Re-apply styles with dependencies
        if hasattr(self, '_apply_all_styles'):
            self._apply_all_styles()
    
    BaseWidget.__init__ = patched_init

# Apply dependency injection
_inject_dependencies()

# Public API exports
__all__ = [
    'App', 'Theme', 'StyleClass',
    'Button', 
    # Add more widgets as they're implemented
]