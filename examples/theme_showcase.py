"""Theme showcase example"""

import sys
import os

# Add the parent directory to the Python path so we can import src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import App
from src.widgets import Button, Entry, Frame, Label

def create_theme_demo(parent, theme_name):
    """Create a demo section for a theme"""
    frame = Frame(
        parent,
        style={
            'bg': '#ffffff',
            'padding': 15,
            'radius': 8,
            'border_width': 1,
            'border_color': '#e0e0e0'
        }
    )
    
    # Theme label
    Label(
        frame,
        text=f"{theme_name.title()} Theme",
        style={
            'font': ('Segoe UI', 12, 'bold'),
            'fg': '#2c3e50'
        }
    ).pack(pady=(0, 10))
    
    # Sample buttons
    Button(
        frame,
        text="Primary Button",
        style={
            'bg': '#0078d4' if theme_name == 'default' else '#1976d2' if theme_name == 'material' else '#404040',
            'fg': 'white',
            'padding': (12, 6),
            'radius': 4,
            'hover_bg': '#106ebe' if theme_name == 'default' else '#1565c0' if theme_name == 'material' else '#505050'
        }
    ).pack(pady=2)
    
    Button(
        frame,
        text="Secondary Button",
        style={
            'bg': '#6c757d',
            'fg': 'white',
            'padding': (12, 6),
            'radius': 4,
            'hover_bg': '#5a6268'
        }
    ).pack(pady=2)
    
    return frame

def main():
    app = App(theme="dark", title="Modern Dashboard", geometry="1200x800")
    
    # Sidebar
    sidebar = Frame(
        app,
        style={
            'bg': '#2c3e50',
            'width': 250,
            'padding': 20
        }
    )
    sidebar.pack(side='left', fill='y')
    
    # Logo/Title
    Label(
        sidebar,
        text="Dashboard",
        style={
            'font': ('Segoe UI', 16, 'bold'),
            'fg': '#ffffff',
            'bg': '#2c3e50'
        }
    ).pack(pady=(0, 30))
    
    # Navigation buttons
    nav_buttons = [
        ("📊 Analytics", lambda: None),
        ("👥 Users", lambda: None),
        ("📈 Reports", lambda: None),
        ("⚙️ Settings", lambda: None)
    ]
    
    for text, command in nav_buttons:
        Button(
            sidebar,
            text=text,
            command=command,
            style={
                'bg': '#34495e',
                'fg': '#ecf0f1',
                'font': ('Segoe UI', 10),
                'padding': (15, 10),
                'radius': 6,
                'hover_bg': '#4a6741',
                'border_width': 0,
                'anchor': 'w'
            }
        ).pack(fill='x', pady=2)
    
    # Main content area
    content = Frame(
        app,
        style={
            'bg': '#ecf0f1',
            'padding': 30
        }
    )
    content.pack(side='right', fill='both', expand=True)
    
    # Header
    header = Frame(
        content,
        style={
            'bg': '#ffffff',
            'padding': 20,
            'radius': 10,
            'border_width': 1,
            'border_color': '#bdc3c7'
        }
    )
    header.pack(fill='x', pady=(0, 20))
    
    Label(
        header,
        text="Analytics Overview",
        style={
            'font': ('Segoe UI', 20, 'bold'),
            'fg': '#2c3e50',
            'bg': '#ffffff'
        }
    ).pack(side='left')
    
    # Stats cards
    stats_frame = Frame(content)
    stats_frame.pack(fill='x', pady=(0, 20))
    
    stats = [
        ("Total Users", "1,234", "#3498db"),
        ("Revenue", "$45,678", "#2ecc71"),
        ("Orders", "890", "#e74c3c"),
        ("Growth", "+12%", "#f39c12")
    ]
    
    for i, (title, value, color) in enumerate(stats):
        card = Frame(
            stats_frame,
            style={
                'bg': '#ffffff',
                'padding': 20,
                'radius': 10,
                'border_width': 1,
                'border_color': '#bdc3c7'
            }
        )
        card.pack(side='left', fill='both', expand=True, padx=(0 if i == 0 else 10, 0))
        
        Label(
            card,
            text=title,
            style={
                'font': ('Segoe UI', 10),
                'fg': '#7f8c8d',
                'bg': '#ffffff'
            }
        ).pack()
        
        Label(
            card,
            text=value,
            style={
                'font': ('Segoe UI', 18, 'bold'),
                'fg': color,
                'bg': '#ffffff'
            }
        ).pack()
    
    # Chart placeholder
    chart_frame = Frame(
        content,
        style={
            'bg': '#ffffff',
            'padding': 30,
            'radius': 10,
            'border_width': 1,
            'border_color': '#bdc3c7',
            'height': 300
        }
    )
    chart_frame.pack(fill='both', expand=True)
    
    Label(
        chart_frame,
        text="📊 Chart Area\n(Chart widgets would go here)",
        style={
            'font': ('Segoe UI', 14),
            'fg': '#95a5a6',
            'bg': '#ffffff'
        }
    ).pack(expand=True)
    
    app.run()

if __name__ == "__main__":
    main()