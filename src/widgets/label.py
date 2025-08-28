"""
Enhanced Label widget with styling support.
"""

import tkinter as tk
from typing import Dict, Any
from ..core.base_widget import BaseWidget

class Label(BaseWidget):
    """Enhanced Label with modern styling"""
    
    def __init__(self, parent=None, text="Label", style=None, style_class=None, **kwargs):
        self.text = text
        super().__init__(parent, style, style_class, **kwargs)
    
    def _create_widget(self, **kwargs) -> tk.Widget:
        """Create the underlying Tkinter Label"""
        custom_kwargs = {'text', 'style', 'style_class'}
        tk_kwargs = {k: v for k, v in kwargs.items() if k not in custom_kwargs}
        
        label = tk.Label(
            self.parent,
            text=self.text,
            **tk_kwargs
        )
        
        return label
    
    def get_default_style(self) -> Dict[str, Any]:
        """Default label styling"""
        return {
            'bg': 'SystemWindow',
            'fg': 'SystemWindowText',
            'font': ('TkDefaultFont', 9, 'normal'),
            'anchor': 'w'
        }
    
    def set_text(self, text: str):
        """Set label text"""
        self.text = text
        self.tk_widget.configure(text=text)
    
    def get_text(self) -> str:
        """Get label text"""
        return self.tk_widget.cget('text')