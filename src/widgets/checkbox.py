"""
Custom Checkbox widget with modern styling.
"""

import tkinter as tk
from typing import Dict, Any, Callable, Optional
from ..core.base_widget import BaseWidget

class Checkbox(BaseWidget):
    """Modern checkbox widget"""
    
    def __init__(self, parent=None, text="Checkbox", variable=None, command=None, style=None, style_class=None, **kwargs):
        self.text = text
        self.variable = variable or tk.BooleanVar()
        self.command = command
        
        super().__init__(parent, style, style_class, **kwargs)
    
    def _create_widget(self, **kwargs) -> tk.Widget:
        """Create the underlying Tkinter Checkbutton"""
        custom_kwargs = {'text', 'variable', 'command', 'style', 'style_class'}
        tk_kwargs = {k: v for k, v in kwargs.items() if k not in custom_kwargs}
        
        checkbox = tk.Checkbutton(
            self.parent,
            text=self.text,
            variable=self.variable,
            command=self.command,
            **tk_kwargs
        )
        
        return checkbox
    
    def get_default_style(self) -> Dict[str, Any]:
        """Default checkbox styling"""
        return {
            'bg': 'SystemWindow',
            'fg': 'SystemWindowText',
            'font': ('TkDefaultFont', 9, 'normal'),
            'anchor': 'w',
            'cursor': 'hand2'
        }
    
    def get_value(self) -> bool:
        """Get checkbox state"""
        return self.variable.get()
    
    def set_value(self, value: bool):
        """Set checkbox state"""
        self.variable.set(value)