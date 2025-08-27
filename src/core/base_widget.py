"""
Base Widget - Abstract foundation for all modern Tkinter widgets
"""

from abc import ABC, abstractmethod
import tkinter as tk
from typing import Dict, Any, Optional, Union

class BaseWidget(ABC):
    """Abstract base class for all modern Tkinter widgets"""
    
    def __init__(self, parent=None, style: Dict[str, Any] = None, 
                 style_class=None, **kwargs):
        self.parent = parent
        self.style_dict = style or {}
        self.style_class = style_class
        self.kwargs = kwargs
        
        # Core components
        self.style_engine = None  # Injected by framework
        self.theme_manager = None  # Injected by framework
        
        # Widget state
        self._is_created = False
        self._event_handlers = {}
        
        # Create the actual Tkinter widget
        self.tk_widget = self._create_widget()
        self._is_created = True
        
        # Apply styling
        self._apply_all_styles()
        
        # Setup event handling
        self._setup_event_handling()
    
    @abstractmethod
    def _create_widget(self) -> tk.Widget:
        """Create the underlying Tkinter widget"""
        pass
    
    @abstractmethod
    def get_default_style(self) -> Dict[str, Any]:
        """Return default style for this widget type"""
        pass
    
    @property
    def widget_type(self) -> str:
        """Return widget type identifier for theme lookup"""
        return self.__class__.__name__.lower()
    
    def _apply_all_styles(self):
        """Apply all styles in correct precedence order"""
        if not self.style_engine:
            return
        
        # Build final style dict with proper inheritance
        final_style = {}
        
        # 1. Widget defaults
        final_style.update(self.get_default_style())
        
        # 2. Theme-based styles
        if self.theme_manager:
            theme_style = self.theme_manager.get_widget_style(self.widget_type)
            if theme_style:
                final_style.update(theme_style)
        
        # 3. Style class
        if self.style_class:
            if hasattr(self.style_class, 'to_dict'):
                final_style.update(self.style_class.to_dict())
            elif isinstance(self.style_class, dict):
                final_style.update(self.style_class)
        
        # 4. Local style overrides
        final_style.update(self.style_dict)
        
        # Apply the computed style
        self.style_engine.apply_style(self.tk_widget, final_style)
    
    def update_style(self, new_style: Dict[str, Any]):
        """Update widget style dynamically"""
        self.style_dict.update(new_style)
        if self._is_created:
            self._apply_all_styles()
    
    def set_style_class(self, style_class):
        """Change the style class of the widget"""
        self.style_class = style_class
        if self._is_created:
            self._apply_all_styles()
    
    def _setup_event_handling(self):
        """Setup enhanced event handling"""
        # Default event handlers can be overridden by subclasses
        pass
    
    def on(self, event: str, handler):
        """Bind event handler"""
        self._event_handlers[event] = handler
        self.tk_widget.bind(event, handler)
        return self
    
    def off(self, event: str):
        """Unbind event handler"""
        if event in self._event_handlers:
            self.tk_widget.unbind(event)
            del self._event_handlers[event]
        return self
    
    # Delegation to underlying Tkinter widget
    def pack(self, **kwargs):
        return self.tk_widget.pack(**kwargs)
    
    def grid(self, **kwargs):
        return self.tk_widget.grid(**kwargs)
    
    def place(self, **kwargs):
        return self.tk_widget.place(**kwargs)
    
    def config(self, **kwargs):
        return self.tk_widget.config(**kwargs)
    
    def cget(self, option):
        return self.tk_widget.cget(option)
    
    def bind(self, event, handler):
        return self.tk_widget.bind(event, handler)
    
    def unbind(self, event):
        return self.tk_widget.unbind(event)
    
    def destroy(self):
        return self.tk_widget.destroy()