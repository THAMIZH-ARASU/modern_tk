"""Icon management utilities for Modern TK"""

import tkinter as tk
from typing import Dict, Any, Optional, Tuple
from PIL import Image, ImageTk
import os

class IconManager:
    """Manages icons for the application"""
    
    def __init__(self):
        self.icons = {}  # {name: PhotoImage}
        self.icon_paths = {}  # {name: file_path}
        self.default_size = (16, 16)
    
    def load_icon(self, name: str, file_path: str, size: Optional[Tuple[int, int]] = None) -> Optional[tk.PhotoImage]:
        """Load an icon from a file"""
        try:
            # Open image with PIL
            image = Image.open(file_path)
            
            # Resize if needed
            if size is None:
                size = self.default_size
            image = image.resize(size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Store references
            self.icons[name] = photo
            self.icon_paths[name] = file_path
            
            return photo
        except Exception as e:
            print(f"Error loading icon {name}: {e}")
            return None
    
    def get_icon(self, name: str) -> Optional[tk.PhotoImage]:
        """Get a loaded icon by name"""
        return self.icons.get(name)
    
    def create_icon_from_text(self, name: str, text: str, size: Tuple[int, int] = None, 
                             font: Tuple[str, int, str] = None, color: str = 'black') -> Optional[tk.PhotoImage]:
        """Create an icon from text"""
        if size is None:
            size = self.default_size
        if font is None:
            font = ('Arial', max(8, size[1] - 4), 'normal')
        
        try:
            # Create image
            image = Image.new('RGBA', size, (0, 0, 0, 0))
            
            # Draw text
            from PIL import ImageDraw
            draw = ImageDraw.Draw(image)
            
            # Get font
            try:
                from PIL import ImageFont
                font_obj = ImageFont.truetype(font[0], font[1])
            except:
                font_obj = ImageFont.load_default()
            
            # Calculate text position
            bbox = draw.textbbox((0, 0), text, font=font_obj)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (size[0] - text_width) // 2
            y = (size[1] - text_height) // 2
            
            # Draw text
            draw.text((x, y), text, fill=color, font=font_obj)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Store reference
            self.icons[name] = photo
            
            return photo
        except Exception as e:
            print(f"Error creating icon from text {name}: {e}")
            return None
    
    def set_default_size(self, width: int, height: int):
        """Set the default icon size"""
        self.default_size = (width, height)
    
    def get_default_size(self) -> Tuple[int, int]:
        """Get the default icon size"""
        return self.default_size
    
    def resize_icon(self, name: str, size: Tuple[int, int]) -> Optional[tk.PhotoImage]:
        """Resize an existing icon"""
        if name in self.icon_paths:
            return self.load_icon(name, self.icon_paths[name], size)
        elif name in self.icons:
            # If we don't have the original path, we can't resize properly
            # In a real implementation, we'd store the original image data
            print(f"Cannot resize icon {name} without original file path")
            return self.icons[name]
        return None
    
    def remove_icon(self, name: str):
        """Remove an icon from memory"""
        if name in self.icons:
            del self.icons[name]
        if name in self.icon_paths:
            del self.icon_paths[name]
    
    def list_icons(self) -> list:
        """List all loaded icons"""
        return list(self.icons.keys())
    
    def clear_icons(self):
        """Clear all loaded icons"""
        self.icons.clear()
        self.icon_paths.clear()

# Global icon manager instance
icon_manager = IconManager()