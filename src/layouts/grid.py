"""Responsive grid layout manager"""

import tkinter as tk
from typing import Dict, Any, List, Tuple, Union
from ..core.base_widget import BaseWidget

class ResponsiveGrid(BaseWidget):
    """Responsive grid layout manager"""
    
    def __init__(self, parent=None, columns=1, rows=1, style=None, style_class=None, **kwargs):
        self.columns = columns
        self.rows = rows
        self.children = []
        self.child_grid_info = {}  # Store grid properties for each child
        self.column_weights = [1] * columns  # Default weight for each column
        self.row_weights = [1] * rows        # Default weight for each row
        
        super().__init__(parent, style, style_class, **kwargs)
        
        # Configure grid weights
        self._configure_grid_weights()
    
    def _create_widget(self, **kwargs) -> tk.Widget:
        """Create the underlying container frame"""
        custom_kwargs = {'columns', 'rows', 'style', 'style_class'}
        tk_kwargs = {k: v for k, v in kwargs.items() if k not in custom_kwargs}
        
        frame = tk.Frame(self.parent, **tk_kwargs)
        return frame
    
    def get_default_style(self) -> Dict[str, Any]:
        """Default grid container styling"""
        return {
            'bg': 'SystemWindow',
            'border_width': 0
        }
    
    def _configure_grid_weights(self):
        """Configure column and row weights for resizing"""
        for i, weight in enumerate(self.column_weights):
            self.tk_widget.columnconfigure(i, weight=weight)
        
        for i, weight in enumerate(self.row_weights):
            self.tk_widget.rowconfigure(i, weight=weight)
    
    def add(self, widget, column=0, row=0, columnspan=1, rowspan=1, 
            sticky='nsew', padx=0, pady=0, **kwargs):
        """Add a child widget to the grid"""
        self.children.append(widget)
        self.child_grid_info[widget] = {
            'column': column,
            'row': row,
            'columnspan': columnspan,
            'rowspan': rowspan,
            'sticky': sticky,
            'padx': padx,
            'pady': pady,
            'kwargs': kwargs
        }
        
        # Place widget in grid
        widget.grid(
            column=column, row=row,
            columnspan=columnspan, rowspan=rowspan,
            sticky=sticky, padx=padx, pady=pady,
            **kwargs
        )
    
    def remove(self, widget):
        """Remove a child widget"""
        if widget in self.children:
            self.children.remove(widget)
            if widget in self.child_grid_info:
                del self.child_grid_info[widget]
            widget.grid_forget()
    
    def clear(self):
        """Remove all child widgets"""
        for child in self.children[:]:
            self.remove(child)
    
    def set_column_weight(self, column, weight):
        """Set the weight of a column"""
        if 0 <= column < self.columns:
            while len(self.column_weights) <= column:
                self.column_weights.append(1)
            self.column_weights[column] = weight
            self.tk_widget.columnconfigure(column, weight=weight)
    
    def set_row_weight(self, row, weight):
        """Set the weight of a row"""
        if 0 <= row < self.rows:
            while len(self.row_weights) <= row:
                self.row_weights.append(1)
            self.row_weights[row] = weight
            self.tk_widget.rowconfigure(row, weight=weight)
    
    def set_columns(self, columns):
        """Set the number of columns"""
        self.columns = columns
        # Ensure column_weights has enough entries
        while len(self.column_weights) < columns:
            self.column_weights.append(1)
        self._configure_grid_weights()
    
    def set_rows(self, rows):
        """Set the number of rows"""
        self.rows = rows
        # Ensure row_weights has enough entries
        while len(self.row_weights) < rows:
            self.row_weights.append(1)
        self._configure_grid_weights()
    
    def get_children(self) -> List:
        """Get all child widgets"""
        return self.children[:]
    
    def get_cell_widgets(self, column, row) -> List:
        """Get widgets in a specific cell"""
        widgets = []
        for widget in self.children:
            info = self.child_grid_info.get(widget, {})
            if (info.get('column') == column and info.get('row') == row):
                widgets.append(widget)
        return widgets
    
    def reposition(self, widget, column=None, row=None, columnspan=None, 
                   rowspan=None, sticky=None, padx=None, pady=None):
        """Reposition a widget with new grid parameters"""
        if widget in self.children:
            info = self.child_grid_info[widget]
            
            # Update parameters if provided
            if column is not None:
                info['column'] = column
            if row is not None:
                info['row'] = row
            if columnspan is not None:
                info['columnspan'] = columnspan
            if rowspan is not None:
                info['rowspan'] = rowspan
            if sticky is not None:
                info['sticky'] = sticky
            if padx is not None:
                info['padx'] = padx
            if pady is not None:
                info['pady'] = pady
            
            # Remove and re-add widget
            widget.grid_forget()
            widget.grid(
                column=info['column'], row=info['row'],
                columnspan=info['columnspan'], rowspan=info['rowspan'],
                sticky=info['sticky'], padx=info['padx'], pady=info['pady']
            )