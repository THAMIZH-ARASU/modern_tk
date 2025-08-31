"""Animation utilities for Modern TK"""

import tkinter as tk
from typing import Dict, Any, Callable, Optional
import time

class AnimationManager:
    """Manages animations for widgets"""
    
    def __init__(self):
        self.animations = {}  # {widget: {property: animation_id}}
        self.running_animations = {}  # {animation_id: animation_data}
        self._animation_counter = 0
    
    def animate_property(self, widget, property_name: str, start_value, end_value, 
                        duration: int, easing: str = 'linear', callback: Optional[Callable] = None):
        """Animate a widget property"""
        # Cancel any existing animation for this property
        if widget in self.animations and property_name in self.animations[widget]:
            old_animation_id = self.animations[widget][property_name]
            if old_animation_id in self.running_animations:
                old_animation = self.running_animations[old_animation_id]
                widget.tk_widget.after_cancel(old_animation['after_id'])
                del self.running_animations[old_animation_id]
        
        # Create animation data
        self._animation_counter += 1
        animation_id = self._animation_counter
        
        animation_data = {
            'widget': widget,
            'property_name': property_name,
            'start_value': start_value,
            'end_value': end_value,
            'duration': duration,
            'easing': easing,
            'callback': callback,
            'start_time': time.time(),
            'after_id': None
        }
        
        # Store animation reference
        if widget not in self.animations:
            self.animations[widget] = {}
        self.animations[widget][property_name] = animation_id
        self.running_animations[animation_id] = animation_data
        
        # Start animation
        self._run_animation(animation_id)
        
        return animation_id
    
    def _run_animation(self, animation_id: int):
        """Run an animation step"""
        if animation_id not in self.running_animations:
            return
        
        animation_data = self.running_animations[animation_id]
        widget = animation_data['widget']
        property_name = animation_data['property_name']
        start_value = animation_data['start_value']
        end_value = animation_data['end_value']
        duration = animation_data['duration']
        easing = animation_data['easing']
        callback = animation_data['callback']
        start_time = animation_data['start_time']
        
        # Calculate progress
        elapsed = (time.time() - start_time) * 1000  # Convert to milliseconds
        progress = min(1.0, elapsed / duration) if duration > 0 else 1.0
        
        # Apply easing
        eased_progress = self._apply_easing(progress, easing)
        
        # Calculate current value
        if isinstance(start_value, (int, float)) and isinstance(end_value, (int, float)):
            current_value = start_value + (end_value - start_value) * eased_progress
        elif isinstance(start_value, str) and isinstance(end_value, str) and start_value.startswith('#') and end_value.startswith('#'):
            # Color interpolation
            current_value = self._interpolate_color(start_value, end_value, eased_progress)
        else:
            # For other types, jump to end when complete
            current_value = end_value if progress >= 1.0 else start_value
        
        # Apply value to widget
        try:
            widget.tk_widget.configure(**{property_name: current_value})
        except:
            pass
        
        # Continue animation or finish
        if progress < 1.0:
            # Schedule next frame
            after_id = widget.tk_widget.after(16, lambda: self._run_animation(animation_id))  # ~60 FPS
            self.running_animations[animation_id]['after_id'] = after_id
        else:
            # Animation complete
            if widget in self.animations and property_name in self.animations[widget]:
                del self.animations[widget][property_name]
                if not self.animations[widget]:
                    del self.animations[widget]
            
            del self.running_animations[animation_id]
            
            # Call callback if provided
            if callback:
                callback()
    
    def _apply_easing(self, progress: float, easing: str) -> float:
        """Apply easing function to progress"""
        if easing == 'linear':
            return progress
        elif easing == 'ease-in':
            return progress ** 2
        elif easing == 'ease-out':
            return 1 - (1 - progress) ** 2
        elif easing == 'ease-in-out':
            if progress < 0.5:
                return 2 * progress ** 2
            else:
                return 1 - (-2 * progress + 2) ** 2 / 2
        else:
            return progress
    
    def _interpolate_color(self, start_color: str, end_color: str, progress: float) -> str:
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
    
    def stop_animation(self, widget, property_name: str):
        """Stop a specific animation"""
        if widget in self.animations and property_name in self.animations[widget]:
            animation_id = self.animations[widget][property_name]
            if animation_id in self.running_animations:
                animation = self.running_animations[animation_id]
                widget.tk_widget.after_cancel(animation['after_id'])
                del self.running_animations[animation_id]
            del self.animations[widget][property_name]
            if not self.animations[widget]:
                del self.animations[widget]
    
    def stop_all_animations(self, widget):
        """Stop all animations for a widget"""
        if widget in self.animations:
            for property_name in list(self.animations[widget].keys()):
                self.stop_animation(widget, property_name)
    
    def is_animating(self, widget, property_name: str) -> bool:
        """Check if a widget property is being animated"""
        return widget in self.animations and property_name in self.animations[widget]