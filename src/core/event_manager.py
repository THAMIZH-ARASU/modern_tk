"""
Enhanced event management system for Modern TK widgets.
Provides hover, focus, and custom event handling.
"""

from typing import Dict, List, Callable, Any
import tkinter as tk

class EventManager:
    """Enhanced event handling for modern widgets"""
    
    def __init__(self):
        self.event_handlers = {}
        self.global_handlers = {}
        self.event_propagation = True
    
    def bind(self, event_name: str, callback: Callable):
        """Bind an event handler"""
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        
        self.event_handlers[event_name].append(callback)
    
    def unbind(self, event_name: str, callback: Callable = None):
        """Unbind event handler(s)"""
        if event_name in self.event_handlers:
            if callback:
                try:
                    self.event_handlers[event_name].remove(callback)
                except ValueError:
                    pass
            else:
                self.event_handlers[event_name] = []
    
    def trigger(self, event_name: str, widget, *args, **kwargs):
        """Trigger an event"""
        # Create event object
        event_obj = ModernEvent(event_name, widget, *args, **kwargs)
        
        # Call widget-specific handlers
        if event_name in self.event_handlers:
            for handler in self.event_handlers[event_name]:
                try:
                    handler(event_obj)
                    if event_obj.stop_propagation:
                        break
                except Exception as e:
                    print(f"Error in event handler: {e}")
        
        # Call global handlers
        if event_name in self.global_handlers:
            for handler in self.global_handlers[event_name]:
                try:
                    handler(event_obj)
                    if event_obj.stop_propagation:
                        break
                except Exception as e:
                    print(f"Error in global event handler: {e}")
    
    def bind_global(self, event_name: str, callback: Callable):
        """Bind a global event handler"""
        if event_name not in self.global_handlers:
            self.global_handlers[event_name] = []
        
        self.global_handlers[event_name].append(callback)
    
    def create_hover_handler(self, enter_callback: Callable = None, leave_callback: Callable = None):
        """Create hover event handlers"""
        def on_enter(event):
            if enter_callback:
                enter_callback(event)
        
        def on_leave(event):
            if leave_callback:
                leave_callback(event)
        
        return on_enter, on_leave
    
    def create_focus_handler(self, focus_in_callback: Callable = None, focus_out_callback: Callable = None):
        """Create focus event handlers"""
        def on_focus_in(event):
            if focus_in_callback:
                focus_in_callback(event)
        
        def on_focus_out(event):
            if focus_out_callback:
                focus_out_callback(event)
        
        return on_focus_in, on_focus_out
    
    def debounce(self, func: Callable, delay: int):
        """Create a debounced version of a function"""
        def debounced_func(*args, **kwargs):
            def call_func():
                func(*args, **kwargs)
            
            if hasattr(debounced_func, '_timer'):
                debounced_func._timer.cancel()
            
            import threading
            debounced_func._timer = threading.Timer(delay / 1000.0, call_func)
            debounced_func._timer.start()
        
        return debounced_func
    
    def throttle(self, func: Callable, interval: int):
        """Create a throttled version of a function"""
        import time
        
        def throttled_func(*args, **kwargs):
            now = time.time()
            if not hasattr(throttled_func, '_last_called'):
                throttled_func._last_called = 0
            
            if now - throttled_func._last_called >= interval / 1000.0:
                throttled_func._last_called = now
                return func(*args, **kwargs)
        
        return throttled_func

class ModernEvent:
    """Enhanced event object for Modern TK"""
    
    def __init__(self, event_name: str, widget, *args, **kwargs):
        self.name = event_name
        self.widget = widget
        self.args = args
        self.kwargs = kwargs
        self.stop_propagation = False
        self.default_prevented = False
        
        import time
        self.timestamp = time.time()
    
    def prevent_default(self):
        """Prevent default event handling"""
        self.default_prevented = True
    
    def stop_propagation(self):
        """Stop event propagation"""
        self.stop_propagation = True