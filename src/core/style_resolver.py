"""
Style inheritance and cascade resolution system.
Handles the complex logic of merging styles from multiple sources.
"""

from typing import Dict, Any, List, Optional

class StyleResolver:
    """Handles style inheritance and cascading"""
    
    def __init__(self, theme_manager=None):
        self.theme_manager = theme_manager
        self.cascade_order = [
            'browser_defaults',
            'theme_defaults',
            'widget_defaults',
            'theme_widget',
            'style_class',
            'local_style',
            'state_overrides'
        ]
    
    def resolve_inheritance(self, widget, local_style: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Resolve style inheritance for a widget"""
        styles = []
        
        # 1. Browser/system defaults (minimal)
        styles.append(self._get_browser_defaults())
        
        # 2. Global theme defaults
        if self.theme_manager:
            styles.append(self.theme_manager.get_theme_value('defaults', {}))
        
        # 3. Widget type defaults
        if hasattr(widget, 'get_default_style'):
            styles.append(widget.get_default_style())
        
        # 4. Theme-specific widget styles
        if self.theme_manager:
            widget_type = widget.__class__.__name__.lower()
            styles.append(self.theme_manager.get_widget_theme(widget_type))
        
        # 5. Style class
        if hasattr(widget, 'style_class') and widget.style_class:
            styles.append(self._extract_style_class(widget.style_class))
        
        # 6. Local style overrides
        if local_style:
            styles.append(local_style)
        
        # 7. State-specific overrides will be handled separately
        
        return self.cascade_merge(styles)
    
    def cascade_merge(self, style_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge styles with proper cascading rules"""
        result = {}
        
        for style_dict in style_list:
            if style_dict:
                result = self._merge_single_style(result, style_dict)
        
        return result
    
    def _merge_single_style(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two style dictionaries"""
        result = base.copy()
        
        for key, value in overlay.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # Deep merge for nested objects
                result[key] = self._merge_single_style(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _get_browser_defaults(self) -> Dict[str, Any]:
        """Get minimal browser/system defaults"""
        return {
            'bg': 'SystemButtonFace',
            'fg': 'SystemButtonText',
            'font': ('TkDefaultFont', 9, 'normal'),
            'border_width': 1,
            'relief': 'raised'
        }
    
    def _extract_style_class(self, style_class) -> Dict[str, Any]:
        """Extract styles from a style class object"""
        style = {}
        
        if hasattr(style_class, '_is_style_class'):
            for attr_name in dir(style_class):
                if not attr_name.startswith('_'):
                    attr_value = getattr(style_class, attr_name)
                    if not callable(attr_value):
                        style[attr_name] = attr_value
        
        return style
    
    def compute_specificity(self, style_source: str) -> int:
        """Compute CSS-like specificity for style sources"""
        specificity_map = {
            'browser_defaults': 0,
            'theme_defaults': 10,
            'widget_defaults': 20,
            'theme_widget': 30,
            'style_class': 40,
            'local_style': 50,
            'state_overrides': 60
        }
        
        return specificity_map.get(style_source, 0)
    
    def resolve_conflicts(self, styles: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve conflicts in style properties"""
        # Handle shorthand vs longhand properties
        resolved = styles.copy()
        
        # Font shorthand
        if 'font' in resolved:
            font = resolved['font']
            if isinstance(font, (tuple, list)) and len(font) >= 3:
                resolved.setdefault('font_family', font[0])
                resolved.setdefault('font_size', font[1])
                resolved.setdefault('font_weight', font[2])
        
        # Padding shorthand
        if 'padding' in resolved:
            padding = resolved['padding']
            if isinstance(padding, (int, float)):
                resolved.setdefault('padx', padding)
                resolved.setdefault('pady', padding)
            elif isinstance(padding, (tuple, list)) and len(padding) >= 2:
                resolved.setdefault('padx', padding[0])
                resolved.setdefault('pady', padding[1])
        
        # Border shorthand
        if 'border' in resolved:
            border = resolved['border']
            if isinstance(border, dict):
                resolved.setdefault('border_width', border.get('width', 1))
                resolved.setdefault('border_color', border.get('color', 'black'))
                resolved.setdefault('border_style', border.get('style', 'solid'))
        
        return resolved