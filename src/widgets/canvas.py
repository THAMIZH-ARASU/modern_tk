"""
Enhanced Canvas widget with styling support.
"""

import tkinter as tk
from typing import Dict, Any
from ..core.base_widget import BaseWidget

class Canvas(BaseWidget):
    """Enhanced Canvas with modern styling"""
    
    def __init__(self, parent=None, style=None, style_class=None, **kwargs):
        super().__init__(parent, style, style_class, **kwargs)
    
    def _create_widget(self, **kwargs) -> tk.Widget:
        """Create the underlying Tkinter Canvas"""
        custom_kwargs = {'style', 'style_class'}
        tk_kwargs = {k: v for k, v in kwargs.items() if k not in custom_kwargs}
        
        canvas = tk.Canvas(self.parent, **tk_kwargs)
        return canvas
    
    def get_default_style(self) -> Dict[str, Any]:
        """Default canvas styling"""
        return {
            'bg': 'white',
            'highlightthickness': 0,
            'relief': 'flat'
        }
    
    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        """Create a rectangle on the canvas"""
        return self.tk_widget.create_rectangle(x1, y1, x2, y2, **kwargs)
    
    def create_oval(self, x1, y1, x2, y2, **kwargs):
        """Create an oval on the canvas"""
        return self.tk_widget.create_oval(x1, y1, x2, y2, **kwargs)
    
    def create_line(self, x1, y1, x2, y2, **kwargs):
        """Create a line on the canvas"""
        return self.tk_widget.create_line(x1, y1, x2, y2, **kwargs)
    
    def create_text(self, x, y, text="", **kwargs):
        """Create text on the canvas"""
        return self.tk_widget.create_text(x, y, text=text, **kwargs)
    
    def create_polygon(self, *points, **kwargs):
        """Create a polygon on the canvas"""
        return self.tk_widget.create_polygon(*points, **kwargs)
    
    def delete(self, item):
        """Delete an item from the canvas"""
        self.tk_widget.delete(item)
    
    def delete_all(self):
        """Delete all items from the canvas"""
        self.tk_widget.delete("all")
    
    def move(self, item, dx, dy):
        """Move an item on the canvas"""
        self.tk_widget.move(item, dx, dy)
    
    def itemconfig(self, item, **kwargs):
        """Configure an item on the canvas"""
        self.tk_widget.itemconfig(item, **kwargs)