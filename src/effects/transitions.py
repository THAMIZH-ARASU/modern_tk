"""Transition effects implementation"""

import tkinter as tk
from typing import Dict, Any, Union
import time

class TransitionEffect:
    """Handles transition effects for widgets"""
    
    def __init__(self):
        self.transition_widgets = {}
        self.animations = {}
    
    def apply(self, widget, transition_config: Union[bool, Dict[str, Any]]):
        """Apply transition effect to a widget"""
        if isinstance(transition_config, bool) and not transition_config:
            self.remove(widget)
            return
        
        # Default transition config
        config = {
            'duration': 300,  # milliseconds
            'easing': 'linear',  # linear, ease-in, ease-out, ease-in-out
            'properties': ['bg', 'fg']  # properties to transition
        }
        
        if isinstance(transition_config, dict):
            config.update(transition_config)
        
        # Store transition config
        self.transition_widgets[widget] = config
    
    def animate_property(self, widget, property_name, start_value, end_value, duration, easing='linear'):
        """Animate a property change"""
        if widget not in self.animations:
            self.animations[widget] = {}
        
        # Cancel any existing animation for this property
        if property_name in self.animations[widget]:
            widget.tk_widget.after_cancel(self.animations[widget][property_name])
        
        # Start new animation
        animation_id = self._run_animation(widget, property_name, start_value, end_value, duration, easing)
        self.animations[widget][property_name] = animation_id
    
    def _run_animation(self, widget, property_name, start_value, end_value, duration, easing):
        """Run property animation"""
        start_time = time.time()
        
        def update_property():
            current_time = time.time()
            elapsed = (current_time - start_time) * 1000  # Convert to milliseconds
            
            if elapsed >= duration:
                # Animation complete
                try:
                    widget.tk_widget.configure(**{property_name: end_value})
                except:
                    pass
                return
            
            # Calculate progress (0.0 to 1.0)
            progress = elapsed / duration
            
            # Apply easing function
            if easing == 'ease-in':
                progress = progress ** 2
            elif easing == 'ease-out':
                progress = 1 - (1 - progress) ** 2
            elif easing == 'ease-in-out':
                if progress < 0.5:
                    progress = 2 * progress ** 2
                else:
                    progress = 1 - (-2 * progress + 2) ** 2 / 2
            
            # Interpolate value
            if isinstance(start_value, str) and start_value.startswith('#') and end_value.startswith('#'):
                # Color interpolation
                new_value = self._interpolate_color(start_value, end_value, progress)
            elif isinstance(start_value, (int, float)) and isinstance(end_value, (int, float)):
                # Numeric interpolation
                new_value = start_value + (end_value - start_value) * progress
            else:
                # For other types, just use end value when complete
                new_value = start_value if progress < 1.0 else end_value
            
            # Apply new value
            try:
                widget.tk_widget.configure(**{property_name: new_value})
            except:
                pass
            
            # Schedule next update
            if elapsed < duration:
                animation_id = widget.tk_widget.after(16, update_property)  # ~60 FPS
                # Store animation ID for this property
                if widget not in self.animations:
                    self.animations[widget] = {}
                self.animations[widget][property_name] = animation_id
        
        # Start animation
        animation_id = widget.tk_widget.after(16, update_property)
        return animation_id
    
    def _interpolate_color(self, start_color, end_color, progress):
        """Interpolate between two hex colors"""
        # Parse start color
        if len(start_color) == 7:  # #RRGGBB
            start_r = int(start_color[1:3], 16)
            start_g = int(start_color[3:5], 16)
            start_b = int(start_color[5:7], 16)
        elif len(start_color) == 4:  # #RGB
            start_r = int(start_color[1:2] + start_color[1:2], 16)
            start_g = int(start_color[2:3] + start_color[2:3], 16)
            start_b = int(start_color[3:4] + start_color[3:4], 16)
        else:
            return start_color
        
        # Parse end color
        if len(end_color) == 7:  # #RRGGBB
            end_r = int(end_color[1:3], 16)
            end_g = int(end_color[3:5], 16)
            end_b = int(end_color[5:7], 16)
        elif len(end_color) == 4:  # #RGB
            end_r = int(end_color[1:2] + end_color[1:2], 16)
            end_g = int(end_color[2:3] + end_color[2:3], 16)
            end_b = int(end_color[3:4] + end_color[3:4], 16)
        else:
            return end_color
        
        # Interpolate
        r = int(start_r + (end_r - start_r) * progress)
        g = int(start_g + (end_g - start_g) * progress)
        b = int(start_b + (end_b - start_b) * progress)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def remove(self, widget):
        """Remove transition from widget"""
        if widget in self.transition_widgets:
            del self.transition_widgets[widget]
        
        # Cancel any running animations
        if widget in self.animations:
            for property_name, animation_id in self.animations[widget].items():
                try:
                    widget.tk_widget.after_cancel(animation_id)
                except:
                    pass
            del self.animations[widget]