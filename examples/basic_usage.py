"""
Basic usage examples for Modern Tkinter Library
Demonstrates the simple, Pythonic API
"""

from src import App, Button, Frame, Label, Theme, StyleClass

# Example 1: Simple styled application
def basic_example():
    """Basic usage with inline styling"""
    app = App(title="Modern Tkinter Demo", theme="default")
    
    # Create a main container
    main_frame = Frame(style={
        'bg': '#f0f0f0',
        'padding': 20
    })
    main_frame.pack(fill='both', expand=True)
    
    # Title label
    title = Label(
        parent=main_frame.tk_widget,
        text="Welcome to Modern Tkinter!",
        style={
            'font': ('Arial', 18, 'bold'),
            'fg': '#333333',
            'bg': '#f0f0f0'
        }
    )
    title.pack(pady=20)
    
    # Styled buttons
    primary_btn = Button(
        parent=main_frame.tk_widget,
        text="Primary Action",
        style={
            'bg': '#007ACC',
            'fg': 'white',
            'font': ('Segoe UI', 11, 'bold'),
            'radius': 8,
            'padding': (20, 10),
            'hover_bg': '#0056b3',
            'shadow': True
        },
        command=lambda: print("Primary button clicked!")
    )
    primary_btn.pack(pady=10)
    
    secondary_btn = Button(
        parent=main_frame.tk_widget,
        text="Secondary Action",
        style={
            'bg': '#6c757d',
            'fg': 'white',
            'font': ('Segoe UI', 11),
            'radius': 8,
            'padding': (20, 10),
            'hover_bg': '#545b62'
        },
        command=lambda: print("Secondary button clicked!")
    )
    secondary_btn.pack(pady=5)
    
    app.run()

# Example 2: Theme-based styling
def theme_example():
    """Using global themes for consistent styling"""
    
    # Create custom theme
    custom_theme = {
        'name': 'Corporate Blue',
        'colors': {
            'primary': '#1e40af',
            'secondary': '#64748b', 
            'success': '#059669',
            'warning': '#d97706',
            'danger': '#dc2626',
            'background': '#f8fafc',
            'surface': '#ffffff',
            'text': '#1e293b',
            'text_secondary': '#64748b',
            'border': '#e2e8f0'
        },
        'widgets': {
            'button': {
                'bg': 'primary',
                'fg': 'white',
                'font': ('Segoe UI', 10, 'bold'),
                'radius': 6,
                'padding': (16, 8),
                'hover_bg': '#1d4ed8',
                'shadow': {'color': 'primary', 'offset': (0, 2), 'blur': 8}
            },
            'frame': {
                'bg': 'surface',
                'relief': 'flat'
            },
            'label': {
                'bg': 'surface',
                'fg': 'text',
                'font': ('Segoe UI', 10)
            }
        }
    }
    
    # Register and use the theme
    Theme.register('corporate', custom_theme)
    
    app = App(title="Theme Example", theme="corporate")
    
    # All widgets automatically inherit theme styles
    main_frame = Frame()
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    title = Label(
        parent=main_frame.tk_widget,
        text="Corporate Theme Demo",
        style={'font': ('Segoe UI', 16, 'bold')}
    )
    title.pack(pady=20)
    
    # Buttons automatically use theme styling
    btn1 = Button(
        parent=main_frame.tk_widget,
        text="Themed Button",
        command=lambda: print("Themed button clicked!")
    )
    btn1.pack(pady=10)
    
    # Override specific properties while keeping theme base
    btn2 = Button(
        parent=main_frame.tk_widget,
        text="Success Button",
        style={'bg': 'success', 'hover_bg': '#047857'},
        command=lambda: print("Success button clicked!")
    )
    btn2.pack(pady=5)
    
    btn3 = Button(
        parent=main_frame.tk_widget,
        text="Warning Button", 
        style={'bg': 'warning', 'hover_bg': '#b45309'},
        command=lambda: print("Warning button clicked!")
    )
    btn3.pack(pady=5)
    
    app.run()

# Example 3: Style Classes (Reusable Styles)
def style_class_example():
    """Using style classes for reusable component styles"""
    
    @StyleClass
    class PrimaryButton:
        bg = '#3b82f6'
        fg = 'white'
        font = ('Segoe UI', 12, 'bold')
        radius = 8
        padding = (20, 10)
        hover_bg = '#2563eb'
        shadow = True
        click_animation = True
    
    @StyleClass
    class SecondaryButton(PrimaryButton):
        bg = '#64748b'
        hover_bg = '#475569'
        shadow = False
    
    @StyleClass
    class DangerButton(PrimaryButton):
        bg = '#ef4444'
        hover_bg = '#dc2626'
    
    @StyleClass
    class CardFrame:
        bg = 'white'
        relief = 'flat'
        radius = 12
        shadow = {'color': '#00000020', 'offset': (0, 4), 'blur': 12}
        padding = 24
    
    app = App(title="Style Classes Demo", theme="default")
    
    # Card container
    card = Frame(style_class=CardFrame)
    card.pack(fill='both', expand=True, padx=20, pady=20)
    
    title = Label(
        parent=card.tk_widget,
        text="Style Classes Example",
        style={'font': ('Arial', 18, 'bold'), 'fg': '#1f2937'}
    )
    title.pack(pady=(0, 20))
    
    # Buttons using style classes
    buttons_frame = Frame(parent=card.tk_widget)
    buttons_frame.pack()
    
    btn1 = Button(
        parent=buttons_frame.tk_widget,
        text="Save Changes",
        style_class=PrimaryButton,
        command=lambda: print("Saving...")
    )
    btn1.pack(side='left', padx=5)
    
    btn2 = Button(
        parent=buttons_frame.tk_widget,
        text="Cancel",
        style_class=SecondaryButton,
        command=lambda: print("Cancelled")
    )
    btn2.pack(side='left', padx=5)
    
    btn3 = Button(
        parent=buttons_frame.tk_widget,
        text="Delete",
        style_class=DangerButton,
        command=lambda: print("Deleting...")
    )
    btn3.pack(side='left', padx=5)
    
    app.run()

# Example 4: Dynamic styling and theme switching
def dynamic_example():
    """Dynamic theme switching and style updates"""
    
    app = App(title="Dynamic Styling Demo")
    
    current_theme = "default"
    
    # Main container
    main_frame = Frame(style={'padding': 20})
    main_frame.pack(fill='both', expand=True)
    
    # Title
    title = Label(
        parent=main_frame.tk_widget,
        text="Dynamic Theme Switcher",
        style={'font': ('Arial', 16, 'bold')}
    )
    title.pack(pady=20)
    
    # Theme info label
    info_label = Label(
        parent=main_frame.tk_widget,
        text=f"Current theme: {current_theme}",
        style={'font': ('Segoe UI', 10)}
    )
    info_label.pack(pady=10)
    
    # Sample content
    content_frame = Frame(
        parent=main_frame.tk_widget,
        style={
            'bg': '#ffffff',
            'radius': 8,
            'padding': 20,
            'shadow': True
        }
    )
    content_frame.pack(fill='x', pady=20)
    
    sample_label = Label(
        parent=content_frame.tk_widget,
        text="This content will change appearance based on the selected theme.",
        style={'font': ('Segoe UI', 10)}
    )
    sample_label.pack()
    
    sample_button = Button(
        parent=content_frame.tk_widget,
        text="Sample Button",
        command=lambda: print("Sample button clicked!")
    )
    sample_button.pack(pady=10)
    
    # Theme switching buttons
    def switch_theme(theme_name):
        nonlocal current_theme
        current_theme = theme_name
        Theme.use(theme_name)
        info_label.set_text(f"Current theme: {theme_name}")
        
        # Force re-render of widgets (in real implementation, this would be automatic)
        print(f"Switched to {theme_name} theme")
    
    theme_frame = Frame(parent=main_frame.tk_widget)
    theme_frame.pack(pady=20)
    
    light_btn = Button(
        parent=theme_frame.tk_widget,
        text="Light Theme",
        style={
            'bg': '#f8f9fa',
            'fg': '#212529',
            'radius': 6,
            'padding': (12, 6)
        },
        command=lambda: switch_theme("default")
    )
    light_btn.pack(side='left', padx=5)
    
    dark_btn = Button(
        parent=theme_frame.tk_widget,
        text="Dark Theme",
        style={
            'bg': '#343a40',
            'fg': '#f8f9fa',
            'radius': 6,
            'padding': (12, 6)
        },
        command=lambda: switch_theme("dark")
    )
    dark_btn.pack(side='left', padx=5)
    
    app.run()

# Example 5: Complete dashboard application
def dashboard_example():
    """Complete example showing a modern dashboard interface"""
    
    @StyleClass
    class SidebarButton:
        bg = '#2d3748'
        fg = '#e2e8f0'
        font = ('Segoe UI', 10)
        relief = 'flat'
        padding = (16, 12)
        hover_bg = '#4a5568'
        text_align = 'left'
    
    @StyleClass
    class StatCard:
        bg = 'white'
        radius = 8
        shadow = {'offset': (0, 2), 'blur': 8, 'color': '#0000001a'}
        padding = 20
    
    @StyleClass
    class PrimaryActionButton:
        bg = '#3182ce'
        fg = 'white'
        font = ('Segoe UI', 10, 'bold')
        radius = 6
        padding = (16, 8)
        hover_bg = '#2c5282'
    
    app = App(title="Modern Dashboard", size=(1200, 800), theme="default")
    
    # Main container
    main_container = Frame(style={'bg': '#f7fafc'})
    main_container.pack(fill='both', expand=True)
    
    # Sidebar
    sidebar = Frame(
        parent=main_container.tk_widget,
        style={
            'bg': '#2d3748',
            'width': 250,
            'padding': 20
        }
    )
    sidebar.pack(side='left', fill='y')
    
    # Sidebar title
    sidebar_title = Label(
        parent=sidebar.tk_widget,
        text="Dashboard",
        style={
            'bg': '#2d3748',
            'fg': 'white',
            'font': ('Segoe UI', 14, 'bold')
        }
    )
    sidebar_title.pack(pady=(0, 30))
    
    # Sidebar navigation
    nav_items = ["Overview", "Analytics", "Reports", "Settings"]
    for item in nav_items:
        btn = Button(
            parent=sidebar.tk_widget,
            text=f"📊 {item}",
            style_class=SidebarButton,
            command=lambda i=item: print(f"Navigating to {i}")
        )
        btn.pack(fill='x', pady=2)
    
    # Main content area
    content_area = Frame(
        parent=main_container.tk_widget,
        style={'bg': '#f7fafc', 'padding': 30}
    )
    content_area.pack(side='right', fill='both', expand=True)
    
    # Header
    header = Frame(parent=content_area.tk_widget, style={'bg': '#f7fafc'})
    header.pack(fill='x', pady=(0, 30))
    
    page_title = Label(
        parent=header.tk_widget,
        text="Analytics Overview",
        style={
            'bg': '#f7fafc',
            'fg': '#2d3748',
            'font': ('Segoe UI', 24, 'bold')
        }
    )
    page_title.pack(side='left')
    
    new_report_btn = Button(
        parent=header.tk_widget,
        text="+ New Report",
        style_class=PrimaryActionButton,
        command=lambda: print("Creating new report...")
    )
    new_report_btn.pack(side='right')
    
    # Stats cards
    stats_frame = Frame(parent=content_area.tk_widget, style={'bg': '#f7fafc'})
    stats_frame.pack(fill='x', pady=(0, 30))
    
    stats_data = [
        ("Total Users", "12,345", "+5.2%"),
        ("Revenue", "$89,123", "+12.8%"),
        ("Conversion", "3.45%", "+0.8%"),
        ("Bounce Rate", "32.1%", "-2.1%")
    ]
    
    for i, (title, value, change) in enumerate(stats_data):
        card = Frame(style_class=StatCard)
        card.pack(side='left', fill='x', expand=True, padx=(0, 15 if i < 3 else 0))
        
        card_title = Label(
            parent=card.tk_widget,
            text=title,
            style={
                'bg': 'white',
                'fg': '#718096',
                'font': ('Segoe UI', 10)
            }
        )
        card_title.pack()
        
        card_value = Label(
            parent=card.tk_widget,
            text=value,
            style={
                'bg': 'white',
                'fg': '#2d3748',
                'font': ('Segoe UI', 20, 'bold')
            }
        )
        card_value.pack()
        
        card_change = Label(
            parent=card.tk_widget,
            text=change,
            style={
                'bg': 'white',
                'fg': '#38a169' if change.startswith('+') else '#e53e3e',
                'font': ('Segoe UI', 10)
            }
        )
        card_change.pack()
    
    # Chart placeholder
    chart_frame = Frame(
        parent=content_area.tk_widget,
        style_class=StatCard
    )
    chart_frame.pack(fill='both', expand=True)
    
    chart_title = Label(
        parent=chart_frame.tk_widget,
        text="Revenue Trends",
        style={
            'bg': 'white',
            'fg': '#2d3748',
            'font': ('Segoe UI', 16, 'bold')
        }
    )
    chart_title.pack(pady=(0, 20))
    
    chart_placeholder = Label(
        parent=chart_frame.tk_widget,
        text="📈 Interactive Chart Would Go Here",
        style={
            'bg': '#f7fafc',
            'fg': '#a0aec0',
            'font': ('Segoe UI', 14),
            'relief': 'solid',
            'borderwidth': 2,
            'padding': 60
        }
    )
    chart_placeholder.pack(fill='both', expand=True)
    
    app.run()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        example = sys.argv[1]
        examples = {
            'basic': basic_example,
            'theme': theme_example,
            'styles': style_class_example,
            'dynamic': dynamic_example,
            'dashboard': dashboard_example
        }
        
        if example in examples:
            examples[example]()
        else:
            print(f"Available examples: {', '.join(examples.keys())}")
    else:
        # Run all examples in sequence for demo
        print("Running Basic Example...")
        basic_example()