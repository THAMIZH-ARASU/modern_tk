"""
Enhanced Frame widget with styling support.
"""

import tkinter as tk
from typing import Dict, Any
from ..core.base_widget import BaseWidget

class Frame(BaseWidget):
    """Enhanced Frame with modern styling"""
    
    def __init__(self, parent=None, style=None, style_class=None, **kwargs):
        super().__init__(parent, style, style_class, **kwargs)
    
    def _create_widget(self, **kwargs) -> tk.Widget:
        """Create the underlying Tkinter Frame"""
        custom_kwargs = {'style', 'style_class'}
        tk_kwargs = {k: v for k, v in kwargs.items() if k not in custom_kwargs}
        
        frame = tk.Frame(self.parent, **tk_kwargs)
        return frame
    
    def get_default_style(self) -> Dict[str, Any]:
        """Default frame styling"""
        return {
            'bg': 'SystemWindow',
            'relief': 'flat',
            'border_width': 0
        }
    
    def add_child(self, child_widget, layout='pack', **layout_kwargs):
        """Add a child widget with layout"""
        if layout == 'pack':
            child_widget.pack(**layout_kwargs)
        elif layout == 'grid':
            child_widget.grid(**layout_kwargs)
        elif layout == 'place':
            child_widget.place(**layout_kwargs)