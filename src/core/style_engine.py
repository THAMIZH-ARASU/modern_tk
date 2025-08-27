"""
Core Style Engine - Translates Pythonic style definitions to Tkinter configurations
"""

import tkinter as tk
from typing import Dict, Any, Optional, Union
from abc import ABC, abstractmethod
import re

class StyleProperty:
    """Represents a style property with validation and processing logic"""
    
    def __init__(self, tk_option: str = None, processor=None, validator=None):
        self.tk_option = tk_option
        self.processor = processor or (lambda x: x)
        self.validator = validator or (lambda x: True)
    
    def process(self, value: Any) -> Any:
        if not self.validator(value):
            raise ValueError(f"Invalid value for style property: {value}")
        return self.processor(value)

class StyleEngine:
    """Core engine for processing and applying styles to widgets"""
    
    def __init__(self):
        self.properties = self._init_style_properties()
        self.theme_manager = None  # Will be injected
        self.special_processors = {
            'radius': self._process_radius,
            'shadow': self._process_shadow,
            'gradient': self._process_gradient,
            'hover_bg': self._process_hover_state,
            'focus_bg': self._process_focus_state,
        }
    
    def _init_style_properties(self) -> Dict[str, StyleProperty]:
        """Initialize mapping of style properties to Tkinter options"""
        return {
            # Basic properties
            'bg': StyleProperty('bg', self._process_color),
            'background': StyleProperty('bg', self._process_color),
            'fg': StyleProperty('fg', self._process_color),
            'foreground': StyleProperty('fg', self._process_color),
            'font': StyleProperty('font', self._process_font),
            'width': StyleProperty('width', int),
            'height': StyleProperty('height', int),
            'relief': StyleProperty('relief'),
            'borderwidth': StyleProperty('borderwidth', int),
            'bd': StyleProperty('bd', int),
            
            # Padding and margins (custom processing)
            'padding': StyleProperty(processor=self._process_padding),
            'margin': StyleProperty(processor=self._process_margin),
            
            # Text properties
            'text_align': StyleProperty('justify'),
            'text_wrap': StyleProperty('wraplength', int),
            
            # State properties (require special handling)
            'hover_bg': StyleProperty(processor=lambda x: x),
            'hover_fg': StyleProperty(processor=lambda x: x),
            'focus_bg': StyleProperty(processor=lambda x: x),
            'active_bg': StyleProperty('activebackground', self._process_color),
            'active_fg': StyleProperty('activeforeground', self._process_color),
            
            # Custom properties (processed separately)
            'radius': StyleProperty(processor=lambda x: max(0, int(x))),
            'shadow': StyleProperty(processor=self._process_shadow_config),
            'gradient': StyleProperty(processor=self._process_gradient_config),
        }
    
    def apply_style(self, widget, style_dict: Dict[str, Any]) -> None:
        """Apply style dictionary to a widget"""
        if not style_dict:
            return
        
        # Separate standard and special properties
        standard_props = {}
        special_props = {}
        
        for key, value in style_dict.items():
            if key in self.special_processors:
                special_props[key] = value
            elif key in self.properties:
                prop = self.properties[key]
                if prop.tk_option:  # Standard Tkinter property
                    try:
                        processed_value = prop.process(value)
                        standard_props[prop.tk_option] = processed_value
                    except (ValueError, TypeError) as e:
                        print(f"Warning: Invalid value for {key}: {value} ({e})")
        
        # Apply standard properties
        if standard_props:
            widget.config(**standard_props)
        
        # Process special properties
        for key, value in special_props.items():
            if key in self.special_processors:
                self.special_processors[key](widget, value)
    
    def _process_color(self, color: Union[str, tuple]) -> str:
        """Process color values - supports hex, rgb tuples, or color names"""
        if isinstance(color, str):
            # Handle theme color references
            if hasattr(self.theme_manager, 'resolve_color'):
                return self.theme_manager.resolve_color(color)
            return color
        elif isinstance(color, tuple) and len(color) == 3:
            # Convert RGB tuple to hex
            r, g, b = [max(0, min(255, int(c))) for c in color]
            return f'#{r:02x}{g:02x}{b:02x}'
        else:
            raise ValueError(f"Invalid color format: {color}")
    
    def _process_font(self, font: Union[str, tuple]) -> tuple:
        """Process font specifications"""
        if isinstance(font, str):
            return (font, 10)
        elif isinstance(font, tuple):
            return font
        else:
            raise ValueError(f"Invalid font format: {font}")
    
    def _process_padding(self, padding: Union[int, tuple]) -> Dict[str, int]:
        """Process padding values (similar to CSS)"""
        if isinstance(padding, int):
            return {'padx': padding, 'pady': padding}
        elif isinstance(padding, tuple):
            if len(padding) == 2:
                return {'padx': padding[0], 'pady': padding[1]}
            elif len(padding) == 4:
                # top, right, bottom, left -> padx, pady
                return {'padx': padding[1], 'pady': padding[0]}
        return {}
    
    def _process_margin(self, margin: Union[int, tuple]) -> Dict[str, int]:
        """Process margin values"""
        # Similar to padding but for external spacing
        return self._process_padding(margin)
    
    def _process_shadow_config(self, shadow_config: Union[bool, dict]) -> dict:
        """Process shadow configuration"""
        if isinstance(shadow_config, bool):
            return {'enabled': shadow_config, 'color': '#888888', 'offset': (2, 2), 'blur': 4}
        elif isinstance(shadow_config, dict):
            defaults = {'enabled': True, 'color': '#888888', 'offset': (2, 2), 'blur': 4}
            defaults.update(shadow_config)
            return defaults
        return {'enabled': False}
    
    def _process_gradient_config(self, gradient_config: Union[list, dict]) -> dict:
        """Process gradient configuration"""
        if isinstance(gradient_config, list) and len(gradient_config) >= 2:
            return {'colors': gradient_config, 'direction': 'vertical'}
        elif isinstance(gradient_config, dict):
            return gradient_config
        return {'enabled': False}
    
    # Special property processors
    def _process_radius(self, widget, radius: int):
        """Apply border radius effect (requires custom canvas overlay)"""
        # Store radius for custom rendering
        if not hasattr(widget, '_modern_tk_effects'):
            widget._modern_tk_effects = {}
        widget._modern_tk_effects['radius'] = radius
        
        # This would trigger custom border rendering
        self._apply_rounded_corners(widget, radius)
    
    def _process_shadow(self, widget, shadow_config: dict):
        """Apply drop shadow effect"""
        if not hasattr(widget, '_modern_tk_effects'):
            widget._modern_tk_effects = {}
        widget._modern_tk_effects['shadow'] = shadow_config
        
        if shadow_config.get('enabled', True):
            self._apply_shadow_effect(widget, shadow_config)
    
    def _process_gradient(self, widget, gradient_config: dict):
        """Apply gradient background"""
        if not hasattr(widget, '_modern_tk_effects'):
            widget._modern_tk_effects = {}
        widget._modern_tk_effects['gradient'] = gradient_config
        
        self._apply_gradient_background(widget, gradient_config)
    
    def _process_hover_state(self, widget, hover_bg: str):
        """Setup hover state styling"""
        original_bg = widget.cget('bg')
        
        def on_enter(event):
            widget.config(bg=self._process_color(hover_bg))
        
        def on_leave(event):
            widget.config(bg=original_bg)
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
    def _process_focus_state(self, widget, focus_bg: str):
        """Setup focus state styling"""
        original_bg = widget.cget('bg')
        
        def on_focus_in(event):
            widget.config(bg=self._process_color(focus_bg))
        
        def on_focus_out(event):
            widget.config(bg=original_bg)
        
        widget.bind('<FocusIn>', on_focus_in)
        widget.bind('<FocusOut>', on_focus_out)
    
    def _apply_rounded_corners(self, widget, radius: int):
        """Apply rounded corners using canvas overlay"""
        # This is a simplified version - real implementation would be more complex
        parent = widget.master
        if parent:
            # Create canvas overlay for rounded effect
            canvas = tk.Canvas(parent, highlightthickness=0)
            # Implementation would draw rounded rectangle
            pass
    
    def _apply_shadow_effect(self, widget, shadow_config: dict):
        """Apply drop shadow effect"""
        # Implementation would create shadow canvas behind widget
        pass
    
    def _apply_gradient_background(self, widget, gradient_config: dict):
        """Apply gradient background using canvas"""
        # Implementation would create gradient canvas
        pass

