"""
Enhanced Scrollbar widget with styling support.
"""

import tkinter as tk
from typing import Dict, Any, Callable
from ..core.base_widget import BaseWidget

class Scrollbar(BaseWidget):
    """Enhanced Scrollbar with modern styling"""
    
    def __init__(self, parent=None, orientation='vertical', command=None, 
                 style=None, style_class=None, **kwargs):
        self.orientation = orientation
        self.command = command
        super().__init__(parent, style, style_class, **kwargs)
    
    def _create_widget(self, **kwargs) -> tk.Widget:
        """Create the underlying Tkinter Scrollbar"""
        custom_kwargs = {'orientation', 'command', 'style', 'style_class'}
        tk_kwargs = {k: v for k, v in kwargs.items() if k not in custom_kwargs}
        
        # Set the orientation for the scrollbar
        if 'orient' not in tk_kwargs:
            tk_kwargs['orient'] = self.orientation
        
        scrollbar = tk.Scrollbar(self.parent, command=self.command, **tk_kwargs)
        return scrollbar
    
    def get_default_style(self) -> Dict[str, Any]:
        """Default scrollbar styling"""
        return {
            'bg': '#f0f0f0',
            'troughcolor': '#e0e0e0',
            'activebackground': '#d0d0d0',
            'highlightthickness': 0,
            'width': 16
        }
    
    def set(self, first, last):
        """Set the scrollbar position"""
        self.tk_widget.set(first, last)
    
    def get(self):
        """Get the scrollbar position"""
        return self.tk_widget.get()
    
    def configure_command(self, command: Callable):
        """Configure the scrollbar command"""
        self.command = command
        self.tk_widget.configure(command=command)
    
    def scroll_to_top(self):
        """Scroll to the top"""
        if self.orientation == 'vertical':
            self.tk_widget.set(0.0, 0.1)
        else:
            self.tk_widget.set(0.0, 0.1)
    
    def scroll_to_bottom(self):
        """Scroll to the bottom"""
        if self.orientation == 'vertical':
            self.tk_widget.set(0.9, 1.0)
        else:
            self.tk_widget.set(0.9, 1.0)