"""
Abstract base class for all Modern TK widgets.
Provides common styling and event handling functionality.
"""

import tkinter as tk
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable
from .style_engine import StyleEngine
from .event_manager import EventManager

class BaseWidget(ABC):
    """Abstract base class for all Modern TK widgets"""
    
    def __init__(self, parent=None, style=None, style_class=None, **kwargs):
        self.parent = parent or tk._default_root
        self.style_dict = style or {}
        self.style_class = style_class
        self.event_manager = EventManager()
        
        # Widget state
        self.state = {
            'normal': True,
            'hover': False,
            'active': False,
            'disabled': False,
            'focused': False
        }
        
        # Style states
        self.style_states = {
            'normal': {},
            'hover': {},
            'active': {},
            'disabled': {},
            'focused': {}
        }
        
        # Extract state-specific styles
        self._extract_state_styles()
        
        # Create the underlying Tkinter widget
        self.tk_widget = self._create_widget(**kwargs)
        
        # Apply initial styling
        self._apply_styles()
        
        # Set up event bindings
        self._setup_events()
    
    @abstractmethod
    def _create_widget(self, **kwargs) -> tk.Widget:
        """Create and return the underlying Tkinter widget"""
        pass
    
    @abstractmethod
    def get_default_style(self) -> Dict[str, Any]:
        """Return default style for this widget type"""
        pass
    
    def _extract_state_styles(self):
        """Extract state-specific styles from the main style dict"""
        for key, value in self.style_dict.items():
            if key.startswith('hover_'):
                state_key = key[6:]  # Remove 'hover_' prefix
                self.style_states['hover'][state_key] = value
            elif key.startswith('active_'):
                state_key = key[7:]  # Remove 'active_' prefix
                self.style_states['active'][state_key] = value
            elif key.startswith('disabled_'):
                state_key = key[9:]  # Remove 'disabled_' prefix
                self.style_states['disabled'][state_key] = value
            elif key.startswith('focused_'):
                state_key = key[8:]  # Remove 'focused_' prefix
                self.style_states['focused'][state_key] = value
            else:
                self.style_states['normal'][key] = value
    
    def _apply_styles(self):
        """Apply current styles to the widget"""
        from . import _global_theme_manager
        
        # Get style engine
        style_engine = StyleEngine(_global_theme_manager)
        
        # Build final style from various sources
        final_style = self._resolve_final_style()
        
        # Apply to widget
        style_engine.apply_to_widget(self, final_style)
    
    def _resolve_final_style(self) -> Dict[str, Any]:
        """Resolve the final style from all sources"""
        final_style = {}
        
        # 1. Default widget style
        final_style.update(self.get_default_style())
        
        # 2. Theme style for this widget type
        from . import _global_theme_manager
        widget_type = self.__class__.__name__.lower()
        theme_style = _global_theme_manager.get_widget_theme(widget_type)
        final_style.update(theme_style)
        
        # 3. Style class
        if self.style_class and hasattr(self.style_class, '_is_style_class'):
            class_style = self._extract_class_style()
            final_style.update(class_style)
        
        # 4. Normal state style
        final_style.update(self.style_states['normal'])
        
        # 5. Current state overlays
        for state, is_active in self.state.items():
            if is_active and state != 'normal':
                final_style.update(self.style_states[state])
        
        return final_style
    
    def _extract_class_style(self) -> Dict[str, Any]:
        """Extract style properties from a style class"""
        style = {}
        
        for attr_name in dir(self.style_class):
            if not attr_name.startswith('_'):
                attr_value = getattr(self.style_class, attr_name)
                if not callable(attr_value):
                    style[attr_name] = attr_value
        
        return style
    
    def _setup_events(self):
        """Set up event bindings for state changes"""
        # Hover events
        self.tk_widget.bind("<Enter>", self._on_enter)
        self.tk_widget.bind("<Leave>", self._on_leave)
        
        # Focus events
        self.tk_widget.bind("<FocusIn>", self._on_focus_in)
        self.tk_widget.bind("<FocusOut>", self._on_focus_out)
        
        # Mouse button events
        self.tk_widget.bind("<ButtonPress-1>", self._on_button_press)
        self.tk_widget.bind("<ButtonRelease-1>", self._on_button_release)
    
    def _on_enter(self, event):
        """Handle mouse enter event"""
        self.state['hover'] = True
        self._apply_styles()
        self.event_manager.trigger('hover_start', self, event)
    
    def _on_leave(self, event):
        """Handle mouse leave event"""
        self.state['hover'] = False
        self._apply_styles()
        self.event_manager.trigger('hover_end', self, event)
    
    def _on_focus_in(self, event):
        """Handle focus in event"""
        self.state['focused'] = True
        self._apply_styles()
        self.event_manager.trigger('focus_in', self, event)
    
    def _on_focus_out(self, event):
        """Handle focus out event"""
        self.state['focused'] = False
        self._apply_styles()
        self.event_manager.trigger('focus_out', self, event)
    
    def _on_button_press(self, event):
        """Handle button press event"""
        self.state['active'] = True
        self._apply_styles()
        self.event_manager.trigger('button_press', self, event)
    
    def _on_button_release(self, event):
        """Handle button release event"""
        self.state['active'] = False
        self._apply_styles()
        self.event_manager.trigger('button_release', self, event)
    
    def update_style(self, style_dict: Dict[str, Any]):
        """Update the widget's style"""
        self.style_dict.update(style_dict)
        self._extract_state_styles()
        self._apply_styles()
    
    def set_state(self, state: str, active: bool = True):
        """Manually set a widget state"""
        if state in self.state:
            self.state[state] = active
            self._apply_styles()
    
    def bind_event(self, event_name: str, callback: Callable):
        """Bind a custom event handler"""
        self.event_manager.bind(event_name, callback)
    
    def trigger_event(self, event_name: str, *args, **kwargs):
        """Trigger a custom event"""
        self.event_manager.trigger(event_name, self, *args, **kwargs)
    
    # Delegate common Tkinter methods
    def pack(self, **kwargs):
        return self.tk_widget.pack(**kwargs)
    
    def grid(self, **kwargs):
        return self.tk_widget.grid(**kwargs)
    
    def place(self, **kwargs):
        return self.tk_widget.place(**kwargs)
    
    def configure(self, **kwargs):
        # Split between style and tkinter options
        style_keys = {'bg', 'fg', 'font', 'radius', 'shadow', 'hover_bg', 'hover_fg'}
        
        style_options = {k: v for k, v in kwargs.items() if k in style_keys}
        tk_options = {k: v for k, v in kwargs.items() if k not in style_keys}
        
        if style_options:
            self.update_style(style_options)
        
        if tk_options:
            return self.tk_widget.configure(**tk_options)
    
    def cget(self, key):
        return self.tk_widget.cget(key)
    
    def __getattr__(self, name):
        """Delegate to the underlying Tkinter widget"""
        return getattr(self.tk_widget, name)