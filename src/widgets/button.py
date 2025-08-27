"""
Modern Button Widget - Enhanced Tkinter Button with modern styling
"""

import tkinter as tk
from ..core.base_widget import BaseWidget
from typing import Dict, Any

class Button(BaseWidget):
    """Modern Button widget with enhanced styling capabilities"""
    
    def __init__(self, parent=None, text="Button", command=None, 
                 style: Dict[str, Any] = None, **kwargs):
        self.text = text
        self.command = command
        
        # Call parent constructor
        super().__init__(parent, style, **kwargs)
    
    def _create_widget(self) -> tk.Button:
        """Create the underlying Tkinter Button"""
        return tk.Button(
            self.parent, 
            text=self.text, 
            command=self.command,
            **{k: v for k, v in self.kwargs.items() if k not in ['style', 'style_class']}
        )
    
    def get_default_style(self) -> Dict[str, Any]:
        """Return default style for Button"""
        return {
            'bg': '#e1e1e1',
            'fg': '#000000',
            'font': ('Segoe UI', 10),
            'relief': 'flat',
            'borderwidth': 0,
            'padding': (12, 6),
            'cursor': 'hand2',
        }
    
    def _setup_event_handling(self):
        """Setup button-specific event handling"""
        super()._setup_event_handling()
        
        # Add click animation if enabled in style
        if self.style_dict.get('click_animation', True):
            self._setup_click_animation()
    
    def _setup_click_animation(self):
        """Setup subtle click animation"""
        def on_button_press(event):
            # Subtle press animation
            self.tk_widget.config(relief='sunken')
        
        def on_button_release(event):
            # Return to normal state
            self.tk_widget.config(relief='flat')
        
        self.tk_widget.bind('<ButtonPress-1>', on_button_press)
        self.tk_widget.bind('<ButtonRelease-1>', on_button_release)
    
    # Button-specific methods
    def click(self):
        """Programmatically trigger button click"""
        if self.command:
            self.command()
    
    def set_text(self, text: str):
        """Update button text"""
        self.text = text
        self.tk_widget.config(text=text)
    
    def get_text(self) -> str:
        """Get current button text"""
        return self.text
    
    def set_command(self, command):
        """Update button command"""
        self.command = command
        self.tk_widget.config(command=command)