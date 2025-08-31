"""Gradient effects implementation"""

import tkinter as tk
from typing import Dict, Any, Union, List

class GradientEffect:
    """Handles gradient effects for widgets"""
    
    def __init__(self):
        self.gradient_widgets = {}
    
    def apply(self, widget, gradient_config: Union[bool, Dict[str, Any]]):
        """Apply gradient effect to a widget"""
        if isinstance(gradient_config, bool) and not gradient_config:
            self.remove(widget)
            return
        
        # Default gradient config
        config = {
            'type': 'linear',  # linear or radial
            'colors': ['#ffffff', '#000000'],
            'direction': 'vertical'  # vertical, horizontal, or angle for linear
        }
        
        if isinstance(gradient_config, dict):
            config.update(gradient_config)
        
        self._create_gradient(widget, config)
    
    def _create_gradient(self, widget, config: Dict[str, Any]):
        """Create gradient effect for widget"""
        # For tkinter, we'll simulate gradients using canvas or color blending
        # This is a simplified implementation
        
        parent = widget.tk_widget.master
        
        # Store gradient reference
        self.gradient_widgets[widget] = {
            'type': config['type'],
            'colors': config['colors'],
            'direction': config['direction']
        }
        
        # For a basic implementation, we'll just set the background color
        # to the first color in the gradient
        if config['colors']:
            widget.tk_widget.configure(bg=config['colors'][0])
        
        # Note: Full implementation would need more sophisticated graphics
        # This is a simplified version for demonstration
    
    def remove(self, widget):
        """Remove gradient from widget"""
        if widget in self.gradient_widgets:
            # Reset to default background
            widget.tk_widget.configure(bg='')
            del self.gradient_widgets[widget]