"""Container widgets for layout management"""

import tkinter as tk
from typing import Dict, Any, List
from ..core.base_widget import BaseWidget

class Container(BaseWidget):
    """Enhanced container with layout capabilities"""
    
    def __init__(self, parent=None, layout='pack', style=None, style_class=None, **kwargs):
        self.layout_type = layout
        self.children = []
        
        super().__init__(parent, style, style_class, **kwargs)
    
    def _create_widget(self, **kwargs) -> tk.Widget:
        """Create the underlying container frame"""
        custom_kwargs = {'layout', 'style', 'style_class'}
        tk_kwargs = {k: v for k, v in kwargs.items() if k not in custom_kwargs}
        
        frame = tk.Frame(self.parent, **tk_kwargs)
        return frame
    
    def get_default_style(self) -> Dict[str, Any]:
        """Default container styling"""
        return {
            'bg': 'SystemWindow',
            'border_width': 0
        }
    
    def add(self, widget, **layout_kwargs):
        """Add a child widget to the container"""
        self.children.append(widget)
        
        if self.layout_type == 'pack':
            widget.pack(**layout_kwargs)
        elif self.layout_type == 'grid':
            widget.grid(**layout_kwargs) 
        elif self.layout_type == 'place':
            widget.place(**layout_kwargs)
    
    def remove(self, widget):
        """Remove a child widget"""
        if widget in self.children:
            self.children.remove(widget)
            widget.pack_forget()  # or grid_forget/place_forget
    
    def clear(self):
        """Remove all child widgets"""
        for child in self.children[:]:
            self.remove(child)