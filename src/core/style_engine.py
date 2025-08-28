"""
Core style processing engine for Modern TK.
Handles style parsing, validation, and application to widgets.
"""

import tkinter as tk
from typing import Dict, Any, Optional, Union
from ..utils.colors import Color
from ..utils.validators import StyleValidator
from ..effects.shadows import ShadowEffect
from ..effects.borders import BorderEffect
from ..effects.gradients import GradientEffect

class StyleEngine:
    """Central style processing and application engine"""
    
    def __init__(self, theme_manager=None):
        self.theme_manager = theme_manager
        self.validator = StyleValidator()
        self.style_cache = {}
        
        # Effect processors
        self.shadow_effect = ShadowEffect()
        self.border_effect = BorderEffect()
        self.gradient_effect = GradientEffect()
    
    def parse_style_dict(self, style_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and normalize a style dictionary"""
        if not style_dict:
            return {}
        
        parsed = {}
        
        for key, value in style_dict.items():
            # Normalize property names
            normalized_key = self._normalize_property_name(key)
            
            # Parse value based on property type
            parsed_value = self._parse_property_value(normalized_key, value)
            
            if parsed_value is not None:
                parsed[normalized_key] = parsed_value
        
        return parsed
    
    def apply_to_widget(self, widget, style_dict: Dict[str, Any]):
        """Apply parsed style to a widget"""
        if not style_dict:
            return
        
        tk_widget = getattr(widget, 'tk_widget', widget)
        
        # Apply basic properties
        self._apply_basic_properties(tk_widget, style_dict)
        
        # Apply special effects
        self._apply_special_effects(widget, style_dict)
    
    def validate_style(self, style_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Validate style properties and values"""
        return self.validator.validate(style_dict)
    
    def cascade_styles(self, *style_dicts) -> Dict[str, Any]:
        """Merge multiple style dictionaries with proper cascading"""
        result = {}
        
        for style_dict in style_dicts:
            if style_dict:
                result.update(style_dict)
        
        return result
    
    def _normalize_property_name(self, prop: str) -> str:
        """Normalize property names (e.g., backgroundColor -> bg)"""
        # CSS-style to Tkinter mapping
        mappings = {
            'backgroundColor': 'bg',
            'foregroundColor': 'fg',
            'textColor': 'fg',
            'fontFamily': 'font_family',
            'fontSize': 'font_size',
            'fontWeight': 'font_weight',
            'borderRadius': 'radius',
            'borderWidth': 'border_width',
            'borderColor': 'border_color',
            'boxShadow': 'shadow',
            'paddingTop': 'pady',
            'paddingLeft': 'padx',
            'marginTop': 'margin_y',
            'marginLeft': 'margin_x',
        }
        
        return mappings.get(prop, prop)
    
    def _parse_property_value(self, prop: str, value: Any) -> Any:
        """Parse property value based on its type"""
        if prop in ['bg', 'fg', 'border_color', 'hover_bg', 'hover_fg']:
            return self._parse_color(value)
        elif prop in ['font_size', 'border_width', 'radius']:
            return self._parse_number(value)
        elif prop == 'font':
            return self._parse_font(value)
        elif prop == 'padding':
            return self._parse_spacing(value)
        elif prop == 'shadow':
            return self._parse_shadow(value)
        else:
            return value
    
    def _parse_color(self, color: Union[str, tuple]) -> str:
        """Parse color value"""
        if isinstance(color, str):
            # Handle theme references
            if self.theme_manager and color.startswith('@'):
                theme_key = color[1:]
                return self.theme_manager.get_theme_value(f"colors.{theme_key}")
            return color
        elif isinstance(color, tuple) and len(color) == 3:
            return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        return str(color)
    
    def _parse_number(self, value: Union[int, float, str]) -> Union[int, float]:
        """Parse numeric value"""
        if isinstance(value, (int, float)):
            return value
        elif isinstance(value, str):
            try:
                if '.' in value:
                    return float(value)
                else:
                    return int(value)
            except ValueError:
                return 0
        return 0
    
    def _parse_font(self, font: Union[str, tuple, list]) -> tuple:
        """Parse font specification"""
        if isinstance(font, str):
            return (font, 10, 'normal')
        elif isinstance(font, (tuple, list)):
            if len(font) >= 3:
                return tuple(font[:3])
            elif len(font) == 2:
                return (font[0], font[1], 'normal')
            elif len(font) == 1:
                return (font[0], 10, 'normal')
        return ('TkDefaultFont', 10, 'normal')
    
    def _parse_spacing(self, value: Union[int, tuple, list]) -> tuple:
        """Parse padding/margin values"""
        if isinstance(value, int):
            return (value, value)
        elif isinstance(value, (tuple, list)):
            if len(value) >= 2:
                return (value[0], value[1])
            elif len(value) == 1:
                return (value[0], value[0])
        return (0, 0)
    
    def _parse_shadow(self, shadow: Union[bool, dict]) -> dict:
        """Parse shadow specification"""
        if isinstance(shadow, bool):
            return {'enabled': shadow} if shadow else {}
        elif isinstance(shadow, dict):
            return shadow
        return {}
    
    def _apply_basic_properties(self, tk_widget, style_dict: Dict[str, Any]):
        """Apply basic Tkinter properties"""
        # Color properties
        if 'bg' in style_dict:
            try:
                tk_widget.configure(bg=style_dict['bg'])
            except tk.TclError:
                pass
        
        if 'fg' in style_dict:
            try:
                tk_widget.configure(fg=style_dict['fg'])
            except tk.TclError:
                pass
        
        # Font properties
        if any(key in style_dict for key in ['font', 'font_family', 'font_size', 'font_weight']):
            font = self._build_font(style_dict)
            try:
                tk_widget.configure(font=font)
            except tk.TclError:
                pass
        
        # Border properties
        if 'border_width' in style_dict:
            try:
                tk_widget.configure(bd=style_dict['border_width'])
            except tk.TclError:
                pass
        
        if 'border_color' in style_dict:
            try:
                tk_widget.configure(highlightbackground=style_dict['border_color'])
            except tk.TclError:
                pass
        
        # Padding
        if 'padx' in style_dict:
            try:
                tk_widget.configure(padx=style_dict['padx'])
            except tk.TclError:
                pass
        
        if 'pady' in style_dict:
            try:
                tk_widget.configure(pady=style_dict['pady'])
            except tk.TclError:
                pass
    
    def _build_font(self, style_dict: Dict[str, Any]) -> tuple:
        """Build font tuple from style properties"""
        if 'font' in style_dict:
            return style_dict['font']
        
        family = style_dict.get('font_family', 'TkDefaultFont')
        size = style_dict.get('font_size', 10)
        weight = style_dict.get('font_weight', 'normal')
        
        return (family, size, weight)
    
    def _apply_special_effects(self, widget, style_dict: Dict[str, Any]):
        """Apply special visual effects"""
        # Shadow effect
        if 'shadow' in style_dict and style_dict['shadow']:
            self.shadow_effect.apply(widget, style_dict['shadow'])
        
        # Border radius
        if 'radius' in style_dict and style_dict['radius'] > 0:
            self.border_effect.apply_radius(widget, style_dict['radius'])
        
        # Gradient background
        if 'gradient' in style_dict:
            self.gradient_effect.apply(widget, style_dict['gradient'])