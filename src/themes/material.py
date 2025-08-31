"""Material Design theme for Modern TK"""

material_theme = {
    "name": "Material Design",
    "version": "1.0",
    
    "colors": {
        "primary": "#1976d2",
        "primary_variant": "#1565c0",
        "secondary": "#03dac6",
        "secondary_variant": "#018786",
        "background": "#ffffff",
        "surface": "#ffffff",
        "error": "#b00020",
        "on_primary": "#ffffff",
        "on_secondary": "#000000",
        "on_background": "#000000",
        "on_surface": "#000000",
        "on_error": "#ffffff",
        
        "success": "#4caf50",
        "warning": "#ff9800",
        "info": "#2196f3",
        "light": "#fafafa",
        "dark": "#212121",
        "border": "#e0e0e0",
        "text": "#212121",
        "text_secondary": "#757575",
        "text_muted": "#9e9e9e"
    },
    
    "fonts": {
        "default": ("Roboto", 9, "normal"),
        "heading": ("Roboto", 12, "medium"),
        "monospace": ("Roboto Mono", 9, "normal"),
        "small": ("Roboto", 8, "normal"),
        "large": ("Roboto", 11, "normal")
    },
    
    "spacing": {
        "xs": 4,
        "sm": 8,
        "md": 16,
        "lg": 24,
        "xl": 32
    },
    
    "borders": {
        "radius": 8,
        "width": 1,
        "color": "#e0e0e0"
    },
    
    "elevation": {
        "0": {"offset": (0, 0), "blur": 0, "color": "#00000000"},
        "1": {"offset": (0, 1), "blur": 3, "color": "#00000033"},
        "2": {"offset": (0, 2), "blur": 6, "color": "#00000029"},
        "3": {"offset": (0, 3), "blur": 10, "color": "#00000026"},
        "4": {"offset": (0, 4), "blur": 14, "color": "#00000024"},
        "6": {"offset": (0, 6), "blur": 20, "color": "#00000021"},
        "8": {"offset": (0, 8), "blur": 25, "color": "#00000020"}
    },
    
    "widgets": {
        "button": {
            "bg": "@colors.primary",
            "fg": "@colors.on_primary",
            "font": ("Roboto", 9, "medium"),
            "border_width": 0,
            "radius": 8,
            "padding": (16, 8),
            "hover_bg": "@colors.primary_variant",
            "shadow": "@elevation.2",
            "text_transform": "uppercase"
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
            "border_width": 0,
            "border_bottom_width": 2,
            "border_color": "@colors.primary",
            "radius": 4,
            "padding": (12, 8),
            "focused_border_color": "@colors.primary",
            "placeholder_fg": "@colors.text_muted"
        },
        
        "text": {
            "bg": "@colors.surface",
            "fg": "@colors.on_surface",
            "font": "@fonts.monospace",
            "border_width": 1,
            "border_color": "@colors.border",
            "radius": 4,
            "shadow": "@elevation.1"
        }
    }
}