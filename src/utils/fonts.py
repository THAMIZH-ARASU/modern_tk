"""Font management utilities"""

import tkinter as tk
from typing import Dict, Any, Optional, Tuple, Union

class FontManager:
    """Font management class"""
    
    def __init__(self):
        self.fonts = {}
        self.default_font = ('TkDefaultFont', 10, 'normal')
    
    def create_font(self, name: str, family: str, size: int, weight: str = 'normal', 
                   slant: str = 'roman', underline: bool = False, overstrike: bool = False) -> Tuple[str, int, str]:
        """Create a font specification"""
        font = (family, size, weight)
        self.fonts[name] = {
            'family': family,
            'size': size,
            'weight': weight,
            'slant': slant,
            'underline': underline,
            'overstrike': overstrike
        }
        return font
    
    def get_font(self, name: str) -> Optional[Tuple[str, int, str]]:
        """Get a font by name"""
        if name in self.fonts:
            font_info = self.fonts[name]
            return (font_info['family'], font_info['size'], font_info['weight'])
        return None
    
    def set_default_font(self, family: str, size: int, weight: str = 'normal'):
        """Set the default font"""
        self.default_font = (family, size, weight)
    
    def get_default_font(self) -> Tuple[str, int, str]:
        """Get the default font"""
        return self.default_font
    
    def scale_font(self, font: Tuple[str, int, str], scale: float) -> Tuple[str, int, str]:
        """Scale a font size"""
        family, size, weight = font
        new_size = int(size * scale)
        return (family, new_size, weight)
    
    def get_font_metrics(self, font: Tuple[str, int, str]) -> Dict[str, int]:
        """Get font metrics (requires a Tk root window)"""
        # This is a simplified implementation
        # In a real implementation, you would use tkFont to get actual metrics
        family, size, weight = font
        return {
            'ascent': int(size * 0.8),
            'descent': int(size * 0.2),
            'linespace': size,
            'fixed': family in ['Courier', 'Courier New', 'Consolas', 'Monaco']
        }
    
    @staticmethod
    def parse_font_string(font_string: str) -> Tuple[str, int, str]:
        """Parse a font string into a font tuple"""
        parts = font_string.split()
        if len(parts) >= 2:
            family = parts[0]
            try:
                size = int(parts[1])
            except ValueError:
                size = 10
            
            weight = 'bold' if 'bold' in parts[2:] else 'normal'
            return (family, size, weight)
        else:
            return ('TkDefaultFont', 10, 'normal')
    
    @staticmethod
    def font_to_string(font: Tuple[str, int, str]) -> str:
        """Convert a font tuple to a string"""
        family, size, weight = font
        return f"{family} {size} {weight}"

# Global font manager instance
font_manager = FontManager()