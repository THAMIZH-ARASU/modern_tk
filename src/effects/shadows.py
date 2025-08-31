"""Shadow effects implementation"""

import tkinter as tk
from typing import Dict, Any, Union

class ShadowEffect:
    """Handles shadow effects for widgets"""
    
    def __init__(self):
        self.shadow_widgets = {}
    
    def apply(self, widget, shadow_config: Union[bool, Dict[str, Any]]):
        """Apply shadow effect to a widget"""
        if isinstance(shadow_config, bool) and not shadow_config:
            self.remove(widget)
            return
        
        # Default shadow config
        config = {
            'offset': (2, 2),
            'blur': 4,
            'color': '#00000030'
        }
        
        if isinstance(shadow_config, dict):
            config.update(shadow_config)
        
        self._create_shadow(widget, config)
    
    def _create_shadow(self, widget, config: Dict[str, Any]):
        """Create shadow widget"""
        # For now, simulate shadow with a frame behind the widget
        # In a full implementation, this would use more sophisticated graphics
        
        parent = widget.tk_widget.master
        
        # Remove existing shadow first
        self.remove(widget)
        
        # Create shadow frame
        shadow_frame = tk.Frame(
            parent,
            bg=config['color'],
            highlightthickness=0,
            bd=0
        )
        
        # Position shadow frame
        x_offset, y_offset = config['offset']
        
        # Get widget position and size
        widget.tk_widget.update_idletasks()
        x = widget.tk_widget.winfo_x()
        y = widget.tk_widget.winfo_y()
        width = widget.tk_widget.winfo_width()
        height = widget.tk_widget.winfo_height()
        
        # Place shadow behind widget
        shadow_frame.place(
            x=x + x_offset,
            y=y + y_offset,
            width=width,
            height=height
        )
        
        # Lower the shadow below the widget
        shadow_frame.lower(widget.tk_widget)
        
        # Store shadow reference
        self.shadow_widgets[widget] = shadow_frame
        
        # Bind to widget events to update shadow position
        widget.tk_widget.bind("<Configure>", lambda e: self._update_shadow_position(widget), add="+")
    
    def _update_shadow_position(self, widget):
        """Update shadow position when widget moves or resizes"""
        if widget in self.shadow_widgets:
            shadow_frame = self.shadow_widgets[widget]
            
            # Get widget position and size
            widget.tk_widget.update_idletasks()
            x = widget.tk_widget.winfo_x()
            y = widget.tk_widget.winfo_y()
            width = widget.tk_widget.winfo_width()
            height = widget.tk_widget.winfo_height()
            
            # Update shadow position
            # Note: We would need to get the offset from stored config for a complete implementation
            shadow_frame.place(
                x=x + 2,  # Default offset
                y=y + 2,
                width=width,
                height=height
            )
    
    def remove(self, widget):
        """Remove shadow from widget"""
        if widget in self.shadow_widgets:
            shadow = self.shadow_widgets[widget]
            shadow.destroy()
            del self.shadow_widgets[widget]
            
            # Unbind events
            try:
                widget.tk_widget.unbind("<Configure>")
            except:
                pass