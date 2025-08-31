"""Fluent Design theme for Modern TK"""

fluent_theme = {
    "name": "Fluent Design",
    "version": "1.0",
    
    "colors": {
        "primary": "#0078d4",
        "primary_variant": "#106ebe",
        "secondary": "#2b88d8",
        "background": "#ffffff",
        "surface": "#f3f2f1",
        "error": "#d13438",
        "on_primary": "#ffffff",
        "on_secondary": "#ffffff",
        "on_background": "#000000",
        "on_surface": "#000000",
        "on_error": "#ffffff",
        
        "success": "#107c10",
        "warning": "#f2c811",
        "info": "#00bcf2",
        "light": "#faf9f8",
        "dark": "#323130",
        "border": "#edebe9",
        "text": "#323130",
        "text_secondary": "#605e5c",
        "text_muted": "#a19f9d"
    },
    
    "fonts": {
        "default": ("Segoe UI", 9, "normal"),
        "heading": ("Segoe UI", 12, "semibold"),
        "monospace": ("Consolas", 9, "normal"),
        "small": ("Segoe UI", 8, "normal"),
        "large": ("Segoe UI", 11, "normal")
    },
    
    "spacing": {
        "xs": 4,
        "sm": 8,
        "md": 12,
        "lg": 16,
        "xl": 24
    },
    
    "borders": {
        "radius": 4,
        "width": 1,
        "color": "#edebe9"
    },
    
    "acrylic": {
        "background": "#f3f2f1a0",  # Semi-transparent background
        "blur": 30
    },
    
    "widgets": {
        "button": {
            "bg": "@colors.primary",
            "fg": "@colors.on_primary",
            "font": "@fonts.default",
            "border_width": 0,
            "radius": 4,
            "padding": (12, 6),
            "hover_bg": "@colors.primary_variant",
            "active_bg": "#005a9e",
            "shadow": False
        },
        
        "frame": {
            "bg": "@colors.background",
            "border_width": 0
        },
        
        "label": {
            "bg": "@colors.background",
            "fg": "@colors.on_background",
            "font": "@fonts.default"
        },
        
        "entry": {
            "bg": "@colors.surface",
            "fg": "@colors.on_surface",
            "font": "@fonts.default",
            "border_width": 1,
            "border_color": "@colors.border",
            "radius": 4,
            "padding": (8, 6),
            "focused_border_color": "@colors.primary",
            "placeholder_fg": "@colors.text_muted"
        },
        
        "text": {
            "bg": "@colors.surface",
            "fg": "@colors.on_surface",
            "font": "@fonts.monospace",
            "border_width": 1,
            "border_color": "@colors.border",
            "radius": 4
        },
        
        "checkbox": {
            "bg": "@colors.background",
            "fg": "@colors.on_background",
            "font": "@fonts.default"
        },
        
        "radiobutton": {
            "bg": "@colors.background",
            "fg": "@colors.on_background",
            "font": "@fonts.default"
        },
        
        "progressbar": {
            "bg": "@colors.surface",
            "fg": "@colors.primary",
            "border_width": 0,
            "radius": 2
        }
    }
}