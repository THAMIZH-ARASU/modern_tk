"""Style validation utilities"""

from typing import Dict, Any, Union, List, Optional
import re

class StyleValidator:
    """Validates style properties and values"""
    
    def __init__(self):
        self.color_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    
    def validate(self, style_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a style dictionary"""
        validated = {}
        errors = []
        
        for prop, value in style_dict.items():
            try:
                validated_value = self.validate_property(prop, value)
                if validated_value is not None:
                    validated[prop] = validated_value
            except ValueError as e:
                errors.append(f"Property '{prop}': {str(e)}")
        
        if errors:
            print(f"Style validation warnings: {', '.join(errors)}")
        
        return validated
    
    def validate_property(self, prop: str, value: Any) -> Any:
        """Validate a single property"""
        # Color properties
        if prop.endswith('_bg') or prop.endswith('_fg') or prop in ['bg', 'fg', 'color', 'border_color']:
            return self.validate_color(value)
        
        # Numeric properties
        elif prop in ['font_size', 'width', 'height', 'border_width', 'radius', 'padx', 'pady', 'opacity']:
            return self.validate_number(value)
        
        # Font property
        elif prop == 'font':
            return self.validate_font(value)
        
        # Boolean properties
        elif prop in ['shadow', 'gradient'] and isinstance(value, bool):
            return value
        
        # Complex properties
        elif prop == 'shadow' and isinstance(value, dict):
            return self.validate_shadow(value)
        
        elif prop == 'gradient' and isinstance(value, dict):
            return self.validate_gradient(value)
        
        # Padding/margin
        elif prop in ['padding', 'margin']:
            return self.validate_spacing(value)
        
        else:
            return value
    
    def validate_color(self, color: Union[str, tuple]) -> str:
        """Validate color value"""
        if isinstance(color, str):
            # Check hex format
            if self.color_pattern.match(color):
                return color
            # Check named colors (basic validation)
            elif color.lower() in ['red', 'green', 'blue', 'white', 'black', 'gray', 'yellow', 'orange', 'purple', 'brown', 'pink', 'cyan', 'magenta']:
                return color
            # Check system colors
            elif color.startswith('System'):
                return color
            else:
                raise ValueError(f"Invalid color format: {color}")
        
        elif isinstance(color, tuple) and len(color) == 3:
            r, g, b = color
            if all(0 <= c <= 255 for c in color):
                return f"#{r:02x}{g:02x}{b:02x}"
            else:
                raise ValueError("RGB values must be 0-255")
        
        else:
            raise ValueError(f"Color must be hex string or RGB tuple, got {type(color)}")
    
    def validate_number(self, value: Union[int, float, str]) -> Union[int, float]:
        """Validate numeric value"""
        if isinstance(value, (int, float)):
            return value
        elif isinstance(value, str):
            try:
                if '.' in value:
                    return float(value)
                else:
                    return int(value)
            except ValueError:
                raise ValueError(f"Invalid number: {value}")
        else:
            raise ValueError(f"Number must be int, float, or string, got {type(value)}")
    
    def validate_font(self, font: Union[str, tuple, list]) -> tuple:
        """Validate font specification"""
        if isinstance(font, str):
            return (font, 10, 'normal')
        elif isinstance(font, (tuple, list)):
            if len(font) >= 3:
                family, size, weight = font[0], font[1], font[2]
                return (str(family), self.validate_number(size), str(weight))
            elif len(font) == 2:
                family, size = font[0], font[1]
                return (str(family), self.validate_number(size), 'normal')
            elif len(font) == 1:
                return (str(font[0]), 10, 'normal')
            else:
                raise ValueError("Font tuple must have 1-3 elements")
        else:
            raise ValueError(f"Font must be string or tuple, got {type(font)}")
    
    def validate_shadow(self, shadow: dict) -> dict:
        """Validate shadow specification"""
        valid_shadow = {}
        
        if 'offset' in shadow:
            offset = shadow['offset']
            if isinstance(offset, (tuple, list)) and len(offset) == 2:
                valid_shadow['offset'] = (self.validate_number(offset[0]), self.validate_number(offset[1]))
            else:
                raise ValueError("Shadow offset must be tuple of 2 numbers")
        
        if 'blur' in shadow:
            valid_shadow['blur'] = self.validate_number(shadow['blur'])
        
        if 'color' in shadow:
            valid_shadow['color'] = self.validate_color(shadow['color'])
        
        return valid_shadow
    
    def validate_gradient(self, gradient: dict) -> dict:
        """Validate gradient specification"""
        valid_gradient = {}
        
        if 'type' in gradient:
            if gradient['type'] in ['linear', 'radial']:
                valid_gradient['type'] = gradient['type']
            else:
                raise ValueError("Gradient type must be 'linear' or 'radial'")
        
        if 'colors' in gradient:
            colors = gradient['colors']
            if isinstance(colors, list) and len(colors) >= 2:
                valid_gradient['colors'] = [self.validate_color(c) for c in colors]
            else:
                raise ValueError("Gradient colors must be list of at least 2 colors")
        
        if 'direction' in gradient:
            valid_gradient['direction'] = gradient['direction']
        
        return valid_gradient
    
    def validate_spacing(self, spacing: Union[int, tuple, list]) -> tuple:
        """Validate spacing (padding/margin) values"""
        if isinstance(spacing, (int, float)):
            return (spacing, spacing)
        elif isinstance(spacing, (tuple, list)):
            if len(spacing) == 1:
                return (spacing[0], spacing[0])
            elif len(spacing) >= 2:
                return (self.validate_number(spacing[0]), self.validate_number(spacing[1]))
            else:
                raise ValueError("Spacing must have 1-2 values")
        else:
            raise ValueError(f"Spacing must be number or tuple, got {type(spacing)}")