"""
Enhanced RadioButton widget with styling support.
"""

import tkinter as tk
from typing import Dict, Any, Callable
from ..core.base_widget import BaseWidget

class RadioButton(BaseWidget):
    """Enhanced RadioButton with modern styling"""
    
    def __init__(self, parent=None, text="RadioButton", variable=None, value=None, 
                 command=None, style=None, style_class=None, **kwargs):
        self.text = text
        self.variable = variable or tk.StringVar()
        self.value = value
        self.command = command
        
        super().__init__(parent, style, style_class, **kwargs)
    
    def _create_widget(self, **kwargs) -> tk.Widget:
        """Create the underlying Tkinter Radiobutton"""
        custom_kwargs = {'text', 'variable', 'value', 'command', 'style', 'style_class'}
        tk_kwargs = {k: v for k, v in kwargs.items() if k not in custom_kwargs}
        
        radiobutton = tk.Radiobutton(
            self.parent,
            text=self.text,
            variable=self.variable,
            value=self.value,
            command=self.command,
            **tk_kwargs
        )
        
        return radiobutton
    
    def get_default_style(self) -> Dict[str, Any]:
        """Default radiobutton styling"""
        return {
            'bg': 'SystemWindow',
            'fg': 'SystemWindowText',
            'font': ('TkDefaultFont', 9, 'normal'),
            'anchor': 'w',
            'cursor': 'hand2'
        }
    
    def get_value(self) -> str:
        """Get the selected value"""
        return self.variable.get()
    
    def set_value(self, value):
        """Set the selected value"""
        self.variable.set(value)
    
    def is_selected(self) -> bool:
        """Check if this radio button is selected"""
        return self.variable.get() == self.value
    
    def select(self):
        """Select this radio button"""
        self.variable.set(self.value)
        if self.command:
            self.command()