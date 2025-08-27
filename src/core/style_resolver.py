"""
Style Resolver - Handles style inheritance and cascading
"""

from typing import Dict, Any, List
import copy

class StyleResolver:
    """Resolves style inheritance and cascading"""
    
    def __init__(self, theme_manager):
        self.theme_manager = theme_manager
    
    def resolve_styles(self, widget_type: str, style_sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Resolve styles from multiple sources with proper cascading
        Sources are applied in order: earlier sources have lower priority
        """
        resolved = {}
        
        for source in style_sources:
            if source:
                resolved.update(self._deep_merge(resolved, source))
        
        # Resolve color references
        resolved = self._resolve_color_references(resolved)
        
        return resolved
    
    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries, with override taking precedence"""
        result = copy.deepcopy(base)
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = copy.deepcopy(value)
        
        return result
    
    def _resolve_color_references(self, style: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve color references in style dictionary"""
        resolved = {}
        
        for key, value in style.items():
            if isinstance(value, str) and self._is_color_property(key):
                resolved[key] = self.theme_manager.resolve_color(value)
            elif isinstance(value, dict):
                resolved[key] = self._resolve_color_references(value)
            else:
                resolved[key] = value
        
        return resolved
    
    def _is_color_property(self, property_name: str) -> bool:
        """Check if a property name represents a color"""
        color_properties = {
            'bg', 'background', 'fg', 'foreground',
            'hover_bg', 'hover_fg', 'focus_bg', 'focus_fg',
            'active_bg', 'active_fg', 'select_bg', 'select_fg',
            'border_color', 'shadow_color'
        }
        return property_name.lower() in color_properties