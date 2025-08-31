"""Flexbox-like layout manager"""

import tkinter as tk
from typing import Dict, Any, List, Union
from ..core.base_widget import BaseWidget

class FlexLayout(BaseWidget):
    """Flexbox-like layout manager"""
    
    def __init__(self, parent=None, direction='row', wrap='nowrap', justify='start', 
                 align='stretch', style=None, style_class=None, **kwargs):
        self.direction = direction  # 'row' or 'column'
        self.wrap = wrap            # 'wrap' or 'nowrap'
        self.justify = justify      # 'start', 'end', 'center', 'space-between', 'space-around'
        self.align = align          # 'stretch', 'start', 'end', 'center', 'baseline'
        self.children = []
        self.child_flex_info = {}   # Store flex properties for each child
        
        super().__init__(parent, style, style_class, **kwargs)
    
    def _create_widget(self, **kwargs) -> tk.Widget:
        """Create the underlying container frame"""
        custom_kwargs = {'direction', 'wrap', 'justify', 'align', 'style', 'style_class'}
        tk_kwargs = {k: v for k, v in kwargs.items() if k not in custom_kwargs}
        
        frame = tk.Frame(self.parent, **tk_kwargs)
        return frame
    
    def get_default_style(self) -> Dict[str, Any]:
        """Default flex container styling"""
        return {
            'bg': 'SystemWindow',
            'border_width': 0
        }
    
    def add(self, widget, flex=0, align_self=None, **kwargs):
        """Add a child widget with flex properties"""
        self.children.append(widget)
        self.child_flex_info[widget] = {
            'flex': flex,
            'align_self': align_self,
            'kwargs': kwargs.copy()
        }
        self._layout_children()
    
    def remove(self, widget):
        """Remove a child widget"""
        if widget in self.children:
            self.children.remove(widget)
            if widget in self.child_flex_info:
                del self.child_flex_info[widget]
            widget.pack_forget()
            self._layout_children()
    
    def clear(self):
        """Remove all child widgets"""
        for child in self.children[:]:
            self.remove(child)
    
    def _layout_children(self):
        """Layout children according to flex properties"""
        # Clear existing layout
        for child in self.children:
            child.pack_forget()
        
        # Apply flex layout
        if self.direction == 'row':
            side = 'left'
            fill = 'y' if self.align == 'stretch' else None
        else:
            side = 'top'
            fill = 'x' if self.align == 'stretch' else None
        
        # Handle flex properties
        total_flex = sum(self.child_flex_info[child].get('flex', 0) for child in self.children)
        
        for child in self.children:
            flex_info = self.child_flex_info[child]
            flex = flex_info.get('flex', 0)
            align_self = flex_info.get('align_self', None)
            kwargs = flex_info.get('kwargs', {})
            
            # Determine expand behavior based on flex
            expand = flex > 0
            
            # Apply packing with flex properties
            pack_kwargs = {
                'side': side,
                'fill': fill,
                'expand': expand
            }
            
            # Override with any specific kwargs
            pack_kwargs.update(kwargs)
            
            child.pack(**pack_kwargs)
    
    def set_direction(self, direction):
        """Set flex direction"""
        self.direction = direction
        self._layout_children()
    
    def set_wrap(self, wrap):
        """Set flex wrap behavior"""
        self.wrap = wrap
        self._layout_children()
    
    def set_justify(self, justify):
        """Set justify content"""
        self.justify = justify
        self._layout_children()
    
    def set_align(self, align):
        """Set align items"""
        self.align = align
        self._layout_children()
    
    def get_children(self) -> List:
        """Get all child widgets"""
        return self.children[:]
    
    def update_layout(self):
        """Manually trigger layout update"""
        self._layout_children()