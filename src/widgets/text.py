"""
Enhanced Text widget with modern styling.
"""

import tkinter as tk
from typing import Dict, Any
from ..core.base_widget import BaseWidget

class Text(BaseWidget):
    """Enhanced Text widget with modern styling"""
    
    def __init__(self, parent=None, style=None, style_class=None, **kwargs):
        super().__init__(parent, style, style_class, **kwargs)
    
    def _create_widget(self, **kwargs) -> tk.Widget:
        """Create the underlying Tkinter Text"""
        custom_kwargs = {'style', 'style_class'}
        tk_kwargs = {k: v for k, v in kwargs.items() if k not in custom_kwargs}
        
        text = tk.Text(self.parent, **tk_kwargs)
        return text
    
    def get_default_style(self) -> Dict[str, Any]:
        """Default text styling"""
        return {
            'bg': 'white',
            'fg': '#333333',
            'font': ('Consolas', 10, 'normal'),
            'border_width': 1,
            'relief': 'solid',
            'wrap': 'word'
        }