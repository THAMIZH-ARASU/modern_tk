"""Responsive layout manager"""

import tkinter as tk
from typing import Dict, Any, List, Callable, Tuple
from ..core.base_widget import BaseWidget

class ResponsiveManager:
    """Manages responsive layout behavior"""
    
    def __init__(self, root_widget=None):
        self.root_widget = root_widget
        self.breakpoints = {}  # {name: width}
        self.layout_configs = {}  # {widget: {breakpoint: config}}
        self.current_breakpoint = None
        self.resize_handlers = []  # List of (widget, handler) tuples
        self.orientation_handlers = []  # List of (widget, handler) tuples
        
        # Default breakpoints
        self.set_breakpoint('mobile', 0)
        self.set_breakpoint('tablet', 768)
        self.set_breakpoint('desktop', 1024)
        self.set_breakpoint('large', 1440)
        
        # Bind to root widget resize events if provided
        if self.root_widget:
            self.root_widget.bind('<Configure>', self._on_resize)
    
    def set_breakpoint(self, name: str, width: int):
        """Define a breakpoint"""
        self.breakpoints[name] = width
    
    def set_layout_config(self, widget, breakpoint_name: str, config: Dict[str, Any]):
        """Set layout configuration for a widget at a specific breakpoint"""
        if widget not in self.layout_configs:
            self.layout_configs[widget] = {}
        self.layout_configs[widget][breakpoint_name] = config
    
    def add_resize_handler(self, widget, handler: Callable):
        """Add a custom resize handler for a widget"""
        self.resize_handlers.append((widget, handler))
    
    def add_orientation_handler(self, widget, handler: Callable):
        """Add a custom orientation change handler for a widget"""
        self.orientation_handlers.append((widget, handler))
    
    def _on_resize(self, event):
        """Handle resize events"""
        if event.widget != self.root_widget:
            return
            
        # Determine current breakpoint
        new_breakpoint = self._get_current_breakpoint(event.width)
        
        # Apply layout changes if breakpoint changed
        if new_breakpoint != self.current_breakpoint:
            self.current_breakpoint = new_breakpoint
            self._apply_breakpoint_layouts(new_breakpoint)
        
        # Call custom resize handlers
        for widget, handler in self.resize_handlers:
            handler(event.width, event.height)
    
    def _get_current_breakpoint(self, width: int) -> str:
        """Get the current breakpoint based on width"""
        # Sort breakpoints by width
        sorted_breakpoints = sorted(self.breakpoints.items(), key=lambda x: x[1], reverse=True)
        
        # Find the first breakpoint that matches
        for name, breakpoint_width in sorted_breakpoints:
            if width >= breakpoint_width:
                return name
        
        # Default to first breakpoint
        return sorted_breakpoints[-1][0] if sorted_breakpoints else 'default'
    
    def _apply_breakpoint_layouts(self, breakpoint_name: str):
        """Apply layouts for the current breakpoint"""
        for widget, configs in self.layout_configs.items():
            if breakpoint_name in configs:
                config = configs[breakpoint_name]
                self._apply_widget_config(widget, config)
    
    def _apply_widget_config(self, widget, config: Dict[str, Any]):
        """Apply configuration to a widget"""
        # Handle packing
        if 'pack' in config:
            pack_config = config['pack']
            # Remove from any existing layout
            widget.pack_forget()
            widget.grid_forget()
            widget.place_forget()
            # Apply new packing
            widget.pack(**pack_config)
        
        # Handle gridding
        elif 'grid' in config:
            grid_config = config['grid']
            # Remove from any existing layout
            widget.pack_forget()
            widget.grid_forget()
            widget.place_forget()
            # Apply new gridding
            widget.grid(**grid_config)
        
        # Handle placing
        elif 'place' in config:
            place_config = config['place']
            # Remove from any existing layout
            widget.pack_forget()
            widget.grid_forget()
            widget.place_forget()
            # Apply new placing
            widget.place(**place_config)
        
        # Handle widget configuration
        if 'configure' in config:
            widget.configure(**config['configure'])
        
        # Handle visibility
        if 'visible' in config:
            if config['visible']:
                # Restore previous layout if it was hidden
                pass
            else:
                # Hide widget
                widget.pack_forget()
                widget.grid_forget()
                widget.place_forget()
    
    def hide_widget(self, widget):
        """Hide a widget"""
        widget.pack_forget()
        widget.grid_forget()
        widget.place_forget()
    
    def show_widget(self, widget, layout_type='pack', **layout_kwargs):
        """Show a widget with specified layout"""
        # Remove from all layouts first
        widget.pack_forget()
        widget.grid_forget()
        widget.place_forget()
        
        # Apply specified layout
        if layout_type == 'pack':
            widget.pack(**layout_kwargs)
        elif layout_type == 'grid':
            widget.grid(**layout_kwargs)
        elif layout_type == 'place':
            widget.place(**layout_kwargs)
    
    def get_current_breakpoint(self) -> str:
        """Get the current breakpoint name"""
        if self.current_breakpoint:
            return self.current_breakpoint
        
        # Determine if we have a root widget to check
        if self.root_widget:
            width = self.root_widget.winfo_width()
            return self._get_current_breakpoint(width)
        
        return 'default'
    
    def get_breakpoint_width(self, breakpoint_name: str) -> int:
        """Get the width for a breakpoint"""
        return self.breakpoints.get(breakpoint_name, 0)
    
    def add_breakpoint_rule(self, breakpoint_name: str, widget, config: Dict[str, Any]):
        """Add a rule for a widget at a specific breakpoint"""
        self.set_layout_config(widget, breakpoint_name, config)
    
    def remove_breakpoint_rule(self, breakpoint_name: str, widget):
        """Remove a rule for a widget at a specific breakpoint"""
        if widget in self.layout_configs and breakpoint_name in self.layout_configs[widget]:
            del self.layout_configs[widget][breakpoint_name]
    
    def clear_all_rules(self):
        """Clear all breakpoint rules"""
        self.layout_configs.clear()