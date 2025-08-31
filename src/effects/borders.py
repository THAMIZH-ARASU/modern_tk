"""Border effects implementation"""

import tkinter as tk
from typing import Dict, Any, Union

class BorderEffect:
    """Handles border effects for widgets"""
    
    def __init__(self):
        self.border_widgets = {}
        self.radius_widgets = {}
    
    def apply(self, widget, border_config: Union[bool, Dict[str, Any]]):
        """Apply border effect to a widget"""
        if isinstance(border_config, bool) and not border_config:
            self.remove(widget)
            return
        
        # Default border config
        config = {
            'width': 1,
            'color': '#000000',
            'style': 'solid'  # solid, dashed, dotted
        }
        
        if isinstance(border_config, dict):
            config.update(border_config)
        
        self._create_border(widget, config)
    
    def apply_radius(self, widget, radius: int):
        """Apply border radius effect to a widget"""
        # For tkinter, border radius is simulated using a canvas
        # This is a simplified implementation
        
        # Store radius reference
        self.radius_widgets[widget] = radius
        
        # For a basic implementation, we'll just set a relief style
        # A full implementation would use a canvas to create rounded corners
        try:
            widget.tk_widget.configure(relief='flat')
        except:
            pass
    
    def _create_border(self, widget, config: Dict[str, Any]):
        """Create border for widget"""
        # For tkinter, we'll simulate borders using frames around the widget
        parent = widget.tk_widget.master
        
        # Store border references
        if widget not in self.border_widgets:
            self.border_widgets[widget] = []
        
        # Remove existing borders first
        self.remove(widget)
        
        width = config['width']
        color = config['color']
        
        # Create frames for each side of the border
        # Top border
        top_border = tk.Frame(parent, bg=color, height=width)
        self.border_widgets[widget].append(top_border)
        
        # Bottom border
        bottom_border = tk.Frame(parent, bg=color, height=width)
        self.border_widgets[widget].append(bottom_border)
        
        # Left border
        left_border = tk.Frame(parent, bg=color, width=width)
        self.border_widgets[widget].append(left_border)
        
        # Right border
        right_border = tk.Frame(parent, bg=color, width=width)
        self.border_widgets[widget].append(right_border)
        
        # Note: Full implementation would need more sophisticated positioning
        # This is a simplified version for demonstration
    
    def remove(self, widget):
        """Remove border from widget"""
        if widget in self.border_widgets:
            for border in self.border_widgets[widget]:
                border.destroy()
            del self.border_widgets[widget]
        
        if widget in self.radius_widgets:
            del self.radius_widgets[widget]