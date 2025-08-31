"""
Enhanced ProgressBar widget with styling support.
"""

import tkinter as tk
from typing import Dict, Any
from ..core.base_widget import BaseWidget

class ProgressBar(BaseWidget):
    """Enhanced ProgressBar with modern styling"""
    
    def __init__(self, parent=None, value=0, maximum=100, style=None, style_class=None, **kwargs):
        self.value = value
        self.maximum = maximum
        super().__init__(parent, style, style_class, **kwargs)
        self._update_progress()
    
    def _create_widget(self, **kwargs) -> tk.Widget:
        """Create the underlying Tkinter Canvas for progress bar"""
        custom_kwargs = {'value', 'maximum', 'style', 'style_class'}
        tk_kwargs = {k: v for k, v in kwargs.items() if k not in custom_kwargs}
        
        # Use Canvas to create a custom progress bar
        canvas = tk.Canvas(self.parent, **tk_kwargs)
        return canvas
    
    def get_default_style(self) -> Dict[str, Any]:
        """Default progress bar styling"""
        return {
            'bg': '#f0f0f0',
            'fg': '#0078d4',
            'border_width': 1,
            'relief': 'solid',
            'width': 200,
            'height': 20
        }
    
    def _update_progress(self):
        """Update the progress bar display"""
        # Clear the canvas
        self.tk_widget.delete("all")
        
        # Get widget dimensions
        width = self.tk_widget.winfo_width()
        height = self.tk_widget.winfo_height()
        
        # If width or height is 1, it means the widget hasn't been rendered yet
        if width <= 1 or height <= 1:
            width = self.style_dict.get('width', 200)
            height = self.style_dict.get('height', 20)
        
        # Draw background
        self.tk_widget.create_rectangle(0, 0, width, height, 
                                       fill=self.style_dict.get('bg', '#f0f0f0'), 
                                       outline=self.style_dict.get('border_color', '#cccccc'),
                                       width=self.style_dict.get('border_width', 1))
        
        # Calculate progress width
        progress_width = int((self.value / self.maximum) * width) if self.maximum > 0 else 0
        
        # Draw progress
        if progress_width > 0:
            self.tk_widget.create_rectangle(0, 0, progress_width, height,
                                           fill=self.style_dict.get('fg', '#0078d4'),
                                           outline="")
    
    def set_value(self, value):
        """Set the progress value"""
        self.value = max(0, min(value, self.maximum))
        self._update_progress()
    
    def get_value(self) -> int:
        """Get the progress value"""
        return self.value
    
    def set_maximum(self, maximum):
        """Set the maximum value"""
        self.maximum = maximum
        if self.value > self.maximum:
            self.value = self.maximum
        self._update_progress()
    
    def get_maximum(self) -> int:
        """Get the maximum value"""
        return self.maximum
    
    def step(self, amount=1):
        """Increment the progress value"""
        self.set_value(self.value + amount)
    
    def start(self, interval=50):
        """Start auto-incrementing the progress bar"""
        def auto_step():
            if self.value < self.maximum:
                self.step()
                self._after_id = self.tk_widget.after(interval, auto_step)
        
        self._after_id = self.tk_widget.after(interval, auto_step)
    
    def stop(self):
        """Stop auto-incrementing the progress bar"""
        if hasattr(self, '_after_id'):
            self.tk_widget.after_cancel(self._after_id)
            delattr(self, '_after_id')