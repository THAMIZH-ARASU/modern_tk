"""
Modern Button widget with enhanced styling and animations.
"""

import tkinter as tk
from typing import Dict, Any, Callable, Optional
from ..core.base_widget import BaseWidget

class Button(BaseWidget):
    """Modern button widget with hover effects and styling"""
    
    def __init__(self, parent=None, text="Button", command=None, style=None, style_class=None, **kwargs):
        self.text = text
        self.command = command
        
        super().__init__(parent, style, style_class, **kwargs)
    
    def _create_widget(self, **kwargs) -> tk.Widget:
        """Create the underlying Tkinter Button"""
        # Extract our custom kwargs
        custom_kwargs = {'text', 'command', 'style', 'style_class'}
        tk_kwargs = {k: v for k, v in kwargs.items() if k not in custom_kwargs}
        
        button = tk.Button(
            self.parent,
            text=self.text,
            command=self.command,
            **tk_kwargs
        )
        
        return button
    
    def get_default_style(self) -> Dict[str, Any]:
        """Default button styling"""
        return {
            'bg': '#f0f0f0',
            'fg': '#333333',
            'font': ('TkDefaultFont', 9, 'normal'),
            'border_width': 1,
            'relief': 'raised',
            'cursor': 'hand2',
            'hover_bg': '#e0e0e0',
            'active_bg': '#d0d0d0',
            'radius': 0,
            'padding': (8, 4)
        }
    
    def _setup_events(self):
        """Set up button-specific events"""
        super()._setup_events()
        
        # Add click animation
        self.bind_event('button_press', self._animate_click)
        
        # Custom hover effects
        self.bind_event('hover_start', self._on_hover_start)
        self.bind_event('hover_end', self._on_hover_end)
    
    def _animate_click(self, event):
        """Animate button click"""
        # Store original relief
        original_relief = self.tk_widget.cget('relief')
        
        # Set pressed state
        self.tk_widget.configure(relief='sunken')
        
        # Restore after short delay
        self.tk_widget.after(100, lambda: self.tk_widget.configure(relief=original_relief))
    
    def _on_hover_start(self, event):
        """Handle hover start with smooth transition"""
        if 'hover_bg' in self.style_states['hover']:
            # Could add animation here
            pass
    
    def _on_hover_end(self, event):
        """Handle hover end"""
        if 'hover_bg' in self.style_states['hover']:
            # Could add animation here
            pass
    
    def set_text(self, text: str):
        """Set button text"""
        self.text = text
        self.tk_widget.configure(text=text)
    
    def get_text(self) -> str:
        """Get button text"""
        return self.tk_widget.cget('text')
    
    def set_command(self, command: Callable):
        """Set button command"""
        self.command = command
        self.tk_widget.configure(command=command)
    
    def click(self):
        """Programmatically click the button"""
        if self.command:
            self.command()