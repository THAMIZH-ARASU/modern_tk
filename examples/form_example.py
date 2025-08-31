"""Modern form example with validation"""

import sys
import os

# Add the parent directory to the Python path so we can import src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import App
from src.widgets import Button, Entry, Frame, Label, Checkbox
import tkinter as tk

class ModernForm:
    def __init__(self):
        self.app = App(title="Modern Form", geometry="500x600")
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        main_frame = Frame(
            self.app,
            style={
                'bg': '#f8f9fa',
                'padding': 40
            }
        )
        main_frame.pack(fill='both', expand=True)
        
        # Form title
        Label(
            main_frame,
            text="Contact Form",
            style={
                'font': ('Segoe UI', 20, 'bold'),
                'fg': '#2c3e50',
                'bg': '#f8f9fa'
            }
        ).pack(pady=(0, 30))
        
        # Form fields
        self.create_field(main_frame, "Name", "Enter your full name")
        self.create_field(main_frame, "Email", "Enter your email address")
        self.create_field(main_frame, "Phone", "Enter your phone number")
        
        # Message field
        Label(
            main_frame,
            text="Message",
            style={
                'font': ('Segoe UI', 10, 'bold'),
                'fg': '#2c3e50',
                'bg': '#f8f9fa'
            }
        ).pack(anchor='w', pady=(20, 5))
        
        # Checkbox
        self.subscribe_var = tk.BooleanVar()
        Checkbox(
            main_frame,
            text="Subscribe to newsletter",
            variable=self.subscribe_var,
            style={
                'bg': '#f8f9fa',
                'fg': '#2c3e50',
                'font': ('Segoe UI', 10)
            }
        ).pack(anchor='w', pady=10)
        
        # Buttons
        button_frame = Frame(main_frame, style={'bg': '#f8f9fa'})
        button_frame.pack(fill='x', pady=(30, 0))
        
        Button(
            button_frame,
            text="Submit",
            command=self.submit_form,
            style={
                'bg': '#28a745',
                'fg': 'white',
                'font': ('Segoe UI', 11, 'bold'),
                'padding': (20, 12),
                'radius': 6,
                'hover_bg': '#218838',
                'border_width': 0
            }
        ).pack(side='right')
        
        Button(
            button_frame,
            text="Reset",
            command=self.reset_form,
            style={
                'bg': '#6c757d',
                'fg': 'white',
                'font': ('Segoe UI', 11),
                'padding': (20, 12),
                'radius': 6,
                'hover_bg': '#5a6268',
                'border_width': 0
            }
        ).pack(side='right', padx=(0, 10))
    
    def create_field(self, parent, label_text, placeholder):
        # Field container
        field_frame = Frame(parent, style={'bg': '#f8f9fa'})
        field_frame.pack(fill='x', pady=(0, 15))
        
        # Label
        Label(
            field_frame,
            text=label_text,
            style={
                'font': ('Segoe UI', 10, 'bold'),
                'fg': '#2c3e50',
                'bg': '#f8f9fa'
            }
        ).pack(anchor='w', pady=(0, 5))
        
        # Entry
        entry = Entry(
            field_frame,
            placeholder=placeholder,
            style={
                'font': ('Segoe UI', 10),
                'padding': (12, 10),
                'radius': 6,
                'border_width': 2,
                'border_color': '#e9ecef',
                'focused_border_color': '#0078d4',
                'bg': '#ffffff'
            }
        )
        entry.pack(fill='x')
        
        return entry
    
    def submit_form(self):
        print("Form submitted!")
        # Form validation and submission logic would go here
    
    def reset_form(self):
        print("Form reset!")
        # Form reset logic would go here
    
    def run(self):
        self.app.run()

def main():
    form = ModernForm()
    form.run()

if __name__ == "__main__":
    main()