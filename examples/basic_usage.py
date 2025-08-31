"""Basic usage example for Modern TK"""


from src import App


def main():
    # Create app with dark theme
    app = App(theme="default", title="Modern TK Demo", geometry="400x300")
    
    # Create main container
    main_frame = Frame(
        app,
        style={
            'bg': '#f8f9fa',
            'padding': 20
        }
    )
    main_frame.pack(fill='both', expand=True)
    
    # Title label
    title = Label(
        main_frame,
        text="Welcome to Modern TK!",
        style={
            'font': ('Segoe UI', 16, 'bold'),
            'fg': '#2c3e50',
            'bg': '#f8f9fa'
        }
    )
    title.pack(pady=(0, 20))
    
    # Entry field with placeholder
    entry = Entry(
        main_frame,
        placeholder="Enter your name...",
        style={
            'font': ('Segoe UI', 10),
            'padding': (10, 8),
            'radius': 6,
            'border_width': 2,
            'border_color': '#e9ecef',
            'focused_border_color': '#0078d4'
        }
    )
    entry.pack(fill='x', pady=(0, 15))
    
    # Button with hover effects
    def on_click():
        name = entry.get()
        if name:
            result_label.set_text(f"Hello, {name}!")
        else:
            result_label.set_text("Please enter your name!")
    
    button = Button(
        main_frame,
        text="Say Hello",
        command=on_click,
        style={
            'bg': '#0078d4',
            'fg': 'white',
            'font': ('Segoe UI', 10, 'bold'),
            'padding': (15, 8),
            'radius': 6,
            'hover_bg': '#106ebe',
            'active_bg': '#005a9e',
            'border_width': 0
        }
    )
    button.pack(pady=(0, 15))
    
    # Result label
    result_label = Label(
        main_frame,
        text="Enter your name and click the button!",
        style={
            'font': ('Segoe UI', 10),
            'fg': '#6c757d',
            'bg': '#f8f9fa'
        }
    )
    result_label.pack()
    
    app.run()

if __name__ == "__main__":
    main()