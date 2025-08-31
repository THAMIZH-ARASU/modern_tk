"""Geometry utilities for layout calculations"""

from typing import Tuple, Union, List
import math

class GeometryUtils:
    """Geometry utility functions"""
    
    @staticmethod
    def distance(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate distance between two points"""
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    @staticmethod
    def midpoint(x1: float, y1: float, x2: float, y2: float) -> Tuple[float, float]:
        """Calculate midpoint between two points"""
        return ((x1 + x2) / 2, (y1 + y2) / 2)
    
    @staticmethod
    def angle(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate angle between two points in radians"""
        return math.atan2(y2 - y1, x2 - x1)
    
    @staticmethod
    def rotate_point(x: float, y: float, cx: float, cy: float, angle: float) -> Tuple[float, float]:
        """Rotate a point around a center point"""
        # Translate point to origin
        x -= cx
        y -= cy
        
        # Rotate point
        new_x = x * math.cos(angle) - y * math.sin(angle)
        new_y = x * math.sin(angle) + y * math.cos(angle)
        
        # Translate back
        new_x += cx
        new_y += cy
        
        return (new_x, new_y)
    
    @staticmethod
    def bounding_box(points: List[Tuple[float, float]]) -> Tuple[float, float, float, float]:
        """Calculate bounding box for a set of points"""
        if not points:
            return (0, 0, 0, 0)
        
        min_x = min(point[0] for point in points)
        max_x = max(point[0] for point in points)
        min_y = min(point[1] for point in points)
        max_y = max(point[1] for point in points)
        
        return (min_x, min_y, max_x, max_y)
    
    @staticmethod
    def point_in_rect(x: float, y: float, rect_x: float, rect_y: float, 
                     rect_width: float, rect_height: float) -> bool:
        """Check if point is inside rectangle"""
        return (rect_x <= x <= rect_x + rect_width and 
                rect_y <= y <= rect_y + rect_height)
    
    @staticmethod
    def rect_intersect(rect1_x: float, rect1_y: float, rect1_width: float, rect1_height: float,
                     rect2_x: float, rect2_y: float, rect2_width: float, rect2_height: float) -> bool:
        """Check if two rectangles intersect"""
        return (rect1_x < rect2_x + rect2_width and
                rect1_x + rect1_width > rect2_x and
                rect1_y < rect2_y + rect2_height and
                rect1_y + rect1_height > rect2_y)
    
    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        """Clamp value between min and max"""
        return max(min_val, min(max_val, value))
    
    @staticmethod
    def lerp(start: float, end: float, t: float) -> float:
        """Linear interpolation between start and end"""
        return start + (end - start) * t
    
    @staticmethod
    def scale_rect(x: float, y: float, width: float, height: float, 
                  scale_x: float, scale_y: float) -> Tuple[float, float, float, float]:
        """Scale a rectangle"""
        new_width = width * scale_x
        new_height = height * scale_y
        new_x = x - (new_width - width) / 2
        new_y = y - (new_height - height) / 2
        return (new_x, new_y, new_width, new_height)