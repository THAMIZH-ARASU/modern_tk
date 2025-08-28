"""Default light theme for Modern TK"""

default_theme = {
    "name": "Default Light",
    "version": "1.0",
    
    "colors": {
        "primary": "#0078d4",
        "secondary": "#6c757d", 
        "success": "#28a745",
        "warning": "#ffc107",
        "danger": "#dc3545",
        "info": "#17a2b8",
        "light": "#f8f9fa",
        "dark": "#343a40",
        
        "background": "#ffffff",
        "surface": "#f8f9fa",
        "border": "#dee2e6",
        "text": "#212529",
        "text_secondary": "#6c757d",
        "text_muted": "#adb5bd"
    },
    
    "fonts": {
        "default": ("Segoe UI", 9, "normal"),
        "heading": ("Segoe UI", 12, "bold"),
        "monospace": ("Consolas", 9, "normal"),
        "small": ("Segoe UI", 8, "normal"),
        "large": ("Segoe UI", 11, "normal")
    },
    
    "spacing": {
        "xs": 2,
        "sm": 4,
        "md": 8,
        "lg": 16,
        "xl": 32
    },
    
    "borders": {
        "radius": 4,
        "width": 1,
        "color": "#dee2e6"
    },
    
    "shadows": {
        "small": {
            "offset": (0, 1),
            "blur": 3,
            "color": "#00000020"
        },
        "medium": {
            "offset": (0, 2),
            "blur": 6,
            "color": "#00000030"
        },
        "large": {
            "offset": (0, 4),
            "blur": 12,
            "color": "#00000040"
        }
    },
    
    "widgets": {
        "button": {
            "bg": "#f8f9fa",
            "fg": "#212529", 
            "font": "@fonts.default",
            "border_width": 1,
            "border_color": "@colors.border",
            "radius": "@borders.radius",
            "padding": (12, 6),
            "hover_bg": "#e9ecef",
            "active_bg": "#dee2e6",
            "shadow": "@shadows.small"
        },
        
        "frame": {
            "bg": "@colors.background",
            "border_width": 0
        },
        
        "label": {
            "bg": "@colors.background",
            "fg": "@colors.text",
            "font": "@fonts.default"
        },
        
        "entry": {
            "bg": "#ffffff",
            "fg": "@colors.text",
            "font": "@fonts.default",
            "border_width": 1,
            "border_color": "@colors.border",
            "radius": "@borders.radius",
            "padding": (8, 6),
            "focused_border_color": "@colors.primary",
            "placeholder_fg": "@colors.text_muted"
        },
        
        "text": {
            "bg": "#ffffff",
            "fg": "@colors.text",
            "font": "@fonts.monospace",
            "border_width": 1,
            "border_color": "@colors.border",
            "radius": "@borders.radius"
        },
        
        "checkbox": {
            "bg": "@colors.background",
            "fg": "@colors.text",
            "font": "@fonts.default"
        }
    }
}