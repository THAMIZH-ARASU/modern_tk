"""
Modern Entry widget with enhanced styling and validation.
"""

import tkinter as tk
from typing import Dict, Any, Callable, Optional
from ..core.base_widget import BaseWidget

class Entry(BaseWidget):
    """Modern entry widget with enhanced styling"""
    
    def __init__(self, parent=None, placeholder="", validate_func=None, style=None, style_class=None, **kwargs):
        self.placeholder = placeholder
        self.validate_func = validate_func
        self.placeholder_active = False
        
        super().__init__(parent, style, style_class, **kwargs)
        
        if self.placeholder:
            self._setup_placeholder()
    
    def _create_widget(self, **kwargs) -> tk.Widget:
        """Create the underlying Tkinter Entry"""
        custom_kwargs = {'placeholder', 'validate_func', 'style', 'style_class'}
        tk_kwargs = {k: v for k, v in kwargs.items() if k not in custom_kwargs}
        
        entry = tk.Entry(self.parent, **tk_kwargs)
        return entry
    
    def get_default_style(self) -> Dict[str, Any]:
        """Default entry styling"""
        return {
            'bg': 'white',
            'fg': '#333333',
            'font': ('TkDefaultFont', 9, 'normal'),
            'border_width': 1,
            'relief': 'solid',
            'focused_border_color': '#0078d4',
            'placeholder_fg': '#999999'
        }
    
    def _setup_placeholder(self):
        """Set up placeholder functionality"""
        if self.get() == "":
            self._show_placeholder()
        
        self.tk_widget.bind('<FocusIn>', self._on_entry_focus_in)
        self.tk_widget.bind('<FocusOut>', self._on_entry_focus_out)
    
    def _show_placeholder(self):
        """Show placeholder text"""
        self.tk_widget.delete(0, tk.END)
        self.tk_widget.insert(0, self.placeholder)
        self.tk_widget.configure(fg=self.style_dict.get('placeholder_fg', '#999999'))
        self.placeholder_active = True
    
    def _hide_placeholder(self):
        """Hide placeholder text"""
        if self.placeholder_active:
            self.tk_widget.delete(0, tk.END)
            self.tk_widget.configure(fg=self.style_dict.get('fg', '#333333'))
            self.placeholder_active = False
    
    def _on_entry_focus_in(self, event):
        """Handle focus in for placeholder"""
        self._hide_placeholder()
    
    def _on_entry_focus_out(self, event):
        """Handle focus out for placeholder"""
        if self.get() == "":
            self._show_placeholder()
    
    def get(self) -> str:
        """Get entry value"""
        value = self.tk_widget.get()
        return "" if self.placeholder_active else value
    
    def set(self, value: str):
        """Set entry value"""
        self._hide_placeholder()
        self.tk_widget.delete(0, tk.END)
        self.tk_widget.insert(0, value)
    
    def clear(self):
        """Clear entry"""
        self.tk_widget.delete(0, tk.END)
        if self.placeholder:
            self._show_placeholder()
    
    def validate(self) -> bool:
        """Validate entry content"""
        if self.validate_func:
            return self.validate_func(self.get())
        return True