"""Color manipulation and conversion utilities"""

import colorsys
from typing import Tuple, Union, Optional

class Color:
    """Color manipulation class"""
    
    def __init__(self, color: Union[str, Tuple[int, int, int]]):
        if isinstance(color, str):
            self.hex = color
            self.rgb = self._hex_to_rgb(color)
        elif isinstance(color, tuple) and len(color) == 3:
            self.rgb = color
            self.hex = self._rgb_to_hex(color)
        else:
            raise ValueError("Color must be hex string or RGB tuple")
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex to RGB"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            raise ValueError("Hex color must be 6 characters")
        
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB to hex"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def lighten(self, amount: float) -> 'Color':
        """Lighten the color by amount (0.0 to 1.0)"""
        h, l, s = colorsys.rgb_to_hls(*[x/255.0 for x in self.rgb])
        l = min(1.0, l + amount)
        rgb = colorsys.hls_to_rgb(h, l, s)
        return Color(tuple(int(x * 255) for x in rgb))
    
    def darken(self, amount: float) -> 'Color':
        """Darken the color by amount (0.0 to 1.0)"""
        h, l, s = colorsys.rgb_to_hls(*[x/255.0 for x in self.rgb])
        l = max(0.0, l - amount)
        rgb = colorsys.hls_to_rgb(h, l, s)
        return Color(tuple(int(x * 255) for x in rgb))
    
    def with_alpha(self, alpha: float) -> str:
        """Return color with alpha channel (for rgba)"""
        alpha_int = int(alpha * 255)
        return f"#{self.hex[1:]}{alpha_int:02x}"
    
    def __str__(self) -> str:
        return self.hex

class ColorUtils:
    """Static color utility functions"""
    
    @staticmethod
    def contrast_ratio(color1: Color, color2: Color) -> float:
        """Calculate contrast ratio between two colors"""
        def luminance(color: Color) -> float:
            rgb = [x / 255.0 for x in color.rgb]
            rgb = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in rgb]
            return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
        
        l1 = luminance(color1)
        l2 = luminance(color2)
        
        lighter = max(l1, l2)
        darker = min(l1, l2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    @staticmethod
    def is_dark(color: Color) -> bool:
        """Check if color is dark"""
        # Using relative luminance
        r, g, b = color.rgb
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return luminance < 0.5
    
    @staticmethod
    def blend(color1: Color, color2: Color, ratio: float = 0.5) -> Color:
        """Blend two colors with given ratio"""
        r1, g1, b1 = color1.rgb
        r2, g2, b2 = color2.rgb
        
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)
        
        return Color((r, g, b))
    
    @staticmethod
    def generate_palette(base_color: Color, count: int = 9) -> list:
        """Generate color palette from base color"""
        palette = []
        
        # Generate lighter shades
        for i in range(count // 2, 0, -1):
            amount = (i / (count // 2)) * 0.5
            palette.append(base_color.lighten(amount))
        
        # Add base color
        palette.append(base_color)
        
        # Generate darker shades
        for i in range(1, count // 2 + 1):
            amount = (i / (count // 2)) * 0.5
            palette.append(base_color.darken(amount))
        
        return palette