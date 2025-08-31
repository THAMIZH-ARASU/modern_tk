"""
Enhanced ListBox widget with styling support.
"""

import tkinter as tk
from typing import Dict, Any, List
from ..core.base_widget import BaseWidget

class ListBox(BaseWidget):
    """Enhanced ListBox with modern styling"""
    
    def __init__(self, parent=None, items=None, style=None, style_class=None, **kwargs):
        self.items = items or []
        super().__init__(parent, style, style_class, **kwargs)
        
        # Insert initial items if provided
        if self.items:
            for item in self.items:
                self.insert(tk.END, item)
    
    def _create_widget(self, **kwargs) -> tk.Widget:
        """Create the underlying Tkinter Listbox"""
        custom_kwargs = {'items', 'style', 'style_class'}
        tk_kwargs = {k: v for k, v in kwargs.items() if k not in custom_kwargs}
        
        listbox = tk.Listbox(self.parent, **tk_kwargs)
        return listbox
    
    def get_default_style(self) -> Dict[str, Any]:
        """Default listbox styling"""
        return {
            'bg': 'white',
            'fg': '#333333',
            'font': ('TkDefaultFont', 9, 'normal'),
            'border_width': 1,
            'relief': 'solid',
            'selectbackground': '#0078d4',
            'selectforeground': 'white',
            'highlightthickness': 0
        }
    
    def insert(self, index, item):
        """Insert an item at the specified index"""
        self.tk_widget.insert(index, item)
    
    def delete(self, first, last=None):
        """Delete items from the listbox"""
        self.tk_widget.delete(first, last)
    
    def delete_all(self):
        """Delete all items from the listbox"""
        self.tk_widget.delete(0, tk.END)
    
    def get(self, first, last=None):
        """Get items from the listbox"""
        return self.tk_widget.get(first, last)
    
    def get_all(self) -> List[str]:
        """Get all items from the listbox"""
        return list(self.tk_widget.get(0, tk.END))
    
    def get_selected(self) -> List[str]:
        """Get selected items from the listbox"""
        selection = self.tk_widget.curselection()
        return [self.tk_widget.get(i) for i in selection]
    
    def select(self, index):
        """Select an item by index"""
        self.tk_widget.selection_clear(0, tk.END)
        self.tk_widget.selection_set(index)
        self.tk_widget.activate(index)
    
    def select_all(self):
        """Select all items"""
        self.tk_widget.selection_set(0, tk.END)
    
    def clear_selection(self):
        """Clear selection"""
        self.tk_widget.selection_clear(0, tk.END)
    
    def size(self) -> int:
        """Get the number of items in the listbox"""
        return self.tk_widget.size()
    
    def index(self, item) -> int:
        """Get the index of an item"""
        items = self.get_all()
        try:
            return items.index(item)
        except ValueError:
            return -1