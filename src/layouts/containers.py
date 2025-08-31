"""Container widgets for layout management"""

import tkinter as tk
from typing import Dict, Any, List
from ..core.base_widget import BaseWidget

class Container(BaseWidget):
    """Enhanced container with layout capabilities"""
    
    def __init__(self, parent=None, layout='pack', style=None, style_class=None, **kwargs):
        self.layout_type = layout
        self.children = []
        self.child_layout_info = {}  # Store layout info for each child
        
        super().__init__(parent, style, style_class, **kwargs)
    
    def _create_widget(self, **kwargs) -> tk.Widget:
        """Create the underlying container frame"""
        custom_kwargs = {'layout', 'style', 'style_class'}
        tk_kwargs = {k: v for k, v in kwargs.items() if k not in custom_kwargs}
        
        frame = tk.Frame(self.parent, **tk_kwargs)
        return frame
    
    def get_default_style(self) -> Dict[str, Any]:
        """Default container styling"""
        return {
            'bg': 'SystemWindow',
            'border_width': 0
        }
    
    def add(self, widget, **layout_kwargs):
        """Add a child widget to the container"""
        self.children.append(widget)
        self.child_layout_info[widget] = layout_kwargs.copy()
        
        if self.layout_type == 'pack':
            widget.pack(**layout_kwargs)
        elif self.layout_type == 'grid':
            widget.grid(**layout_kwargs) 
        elif self.layout_type == 'place':
            widget.place(**layout_kwargs)
    
    def remove(self, widget):
        """Remove a child widget"""
        if widget in self.children:
            self.children.remove(widget)
            if widget in self.child_layout_info:
                del self.child_layout_info[widget]
            
            # Hide widget based on current layout type
            if self.layout_type == 'pack':
                widget.pack_forget()
            elif self.layout_type == 'grid':
                widget.grid_forget()
            elif self.layout_type == 'place':
                widget.place_forget()
    
    def clear(self):
        """Remove all child widgets"""
        for child in self.children[:]:
            self.remove(child)
    
    def reposition(self, widget, **layout_kwargs):
        """Reposition a child widget with new layout parameters"""
        if widget in self.children:
            # Update stored layout info
            self.child_layout_info[widget].update(layout_kwargs)
            
            # Remove and re-add with new parameters
            self.remove(widget)
            self.add(widget, **layout_kwargs)
    
    def get_children(self) -> List:
        """Get all child widgets"""
        return self.children[:]
    
    def set_layout(self, layout_type):
        """Change the layout type and re-apply to all children"""
        old_layout = self.layout_type
        self.layout_type = layout_type
        
        # Re-apply all children with their stored layout info
        for child in self.children[:]:
            layout_kwargs = self.child_layout_info.get(child, {})
            # Remove from old layout
            if old_layout == 'pack':
                child.pack_forget()
            elif old_layout == 'grid':
                child.grid_forget()
            elif old_layout == 'place':
                child.place_forget()
            
            # Add to new layout
            if self.layout_type == 'pack':
                child.pack(**layout_kwargs)
            elif self.layout_type == 'grid':
                child.grid(**layout_kwargs)
            elif self.layout_type == 'place':
                child.place(**layout_kwargs)