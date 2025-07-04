"""
Script: EUIL.py
Description: Extensible UI Language - A simple XML-based UI library for tkinter.
Author: IronBill05
Date: 2025-07-04
"""

import tkinter as tk
from tkinter import ttk
import xml.etree.ElementTree as ET

print("\033[H\033[J", end="")
print("EUIL - Extensible UI Language v0.1 \n")

widget_map = {
    # Basic widgets
    "Label": ttk.Label,
    "Button": ttk.Button,
    "Entry": ttk.Entry,
    "Frame": ttk.Frame,
    "Check": ttk.Checkbutton,
    "Combo": ttk.Combobox,
    "List": tk.Listbox,
    "Menu": tk.Menu,
    "Menubtn": ttk.Menubutton,
    "Txt": ttk.Label,
    "OptionMenu": ttk.OptionMenu,
    "Panedwin": ttk.Panedwindow,
    "Progress": ttk.Progressbar,
    "Radio": ttk.Radiobutton,
    "Scale": ttk.Scale,
    "Scroll": ttk.Scrollbar,
    "Scrollbar": ttk.Scrollbar,
    "Separator": ttk.Separator,
    "Sizegrip": ttk.Sizegrip,
    "Spin": ttk.Spinbox,
    "Spinbox": ttk.Spinbox,
    "Text": tk.Text,
    "Notebook": ttk.Notebook,
    "LabelFrame": ttk.LabelFrame,
    "Grid": ttk.Frame,
    "Statusbar": ttk.Label
}

custom_attrs = {
    # Common attributes
    "id",
    "action",
    "command",
    "values",
    "variable",
    "text",
    "label"
}

id_registry = {}

def create_widget(element, parent, handlers):
    tag = element.tag
    widget_class = widget_map.get(tag)
    if widget_class is None:
        print(f"Warning: Unknown widget type: {tag}")
        return None

    # Special case for Menu commands
    if tag == "Command":
        label = element.get('label', '')
        command = element.get('command', '')
        if command in handlers:
            return parent.add_command(label=label, command=handlers[command])
        return parent.add_command(label=label)
    
    # Handle escape sequences in text content
    if element.text:
        element.text = element.text.replace("\\n", "\n")
        element.text = element.text.replace("\\t", "\t")
        element.text = element.text.replace("\\r", "\r")
        element.text = element.text.replace("\\\\", "\\")

    if element.tail:
        element.tail = element.tail.replace("\\n", "\n")
        element.tail = element.tail.replace("\\t", "\t")
        element.tail = element.tail.replace("\\r", "\r")
        element.tail = element.tail.replace("\\\\", "\\")

    if element.get("label"):
        element.attrib["label"] = element.attrib["label"].replace("\\n", "\n")
        element.attrib["label"] = element.attrib["label"].replace("\\t", "\t")
        element.attrib["label"] = element.attrib["label"].replace("\\r", "\r")
        element.attrib["label"] = element.attrib["label"].replace("\\\\", "\\")

    if element.attrib.get("text"):
        element.attrib["text"] = element.attrib["text"].replace("\\n", "\n")
        element.attrib["text"] = element.attrib["text"].replace("\\t", "\t")
        element.attrib["text"] = element.attrib["text"].replace("\\r", "\r")
        element.attrib["text"] = element.attrib["text"].replace("\\\\", "\\")

    # Handle special attributes
    attrs = element.attrib
    kwargs = {}
    
    # Process attributes, converting string values to appropriate types
    for k, v in attrs.items():
        if k in custom_attrs:
            # Skip special attributes that we handle separately
            if k in ["id", "action", "command", "values", "variable"]:
                continue
                
            # Convert numeric values
            if v.isdigit():
                kwargs[k] = int(v)
            # Convert float values (simple check, not perfect)
            elif v.replace('.', '', 1).isdigit() and v.count('.') < 2:
                kwargs[k] = float(v)
            # Convert boolean values
            elif v.lower() in ('true', 'false'):
                kwargs[k] = v.lower() == 'true'
            # Keep string values as is
            else:
                kwargs[k] = v
    
    # Handle special cases for specific widgets
    if tag == "Combo":
        values = attrs.get('values', '').split(',')
        widget = ttk.Combobox(parent, values=values, **kwargs)
    elif tag == "Spinbox" or tag == "Spin":
        from_val = float(attrs.get('from', 0))
        to_val = float(attrs.get('to', 100))
        widget = ttk.Spinbox(parent, from_=from_val, to=to_val, **kwargs)
    elif tag == "Grid":
        # Custom grid layout
        widget = ttk.Frame(parent, **kwargs)
        # Store grid configuration
        widget.grid_config = {
            'columns': int(attrs.get('columns', 1)),
            'row': 0,
            'col': 0,
            'rowspacing': int(attrs.get('rowspacing', 5)),
            'columnspacing': int(attrs.get('columnspacing', 5))
        }
    elif tag == "Notebook":
        widget = ttk.Notebook(parent, **kwargs)
    elif tag == "Text":
        widget = tk.Text(parent, **kwargs)
    elif tag == "Menu":
        # Create the menu widget
        widget = tk.Menu(parent, tearoff=0, **kwargs)
        
        # Store the menu to be attached to the root window later
        if not hasattr(parent, '_menus_to_attach'):
            parent._menus_to_attach = []
        parent._menus_to_attach.append(widget)
        
        # Process menu items
        for child in element:
            if child.tag == "Menu":
                # This is a submenu
                label = child.attrib.get('text', '')
                submenu = tk.Menu(widget, tearoff=0)
                widget.add_cascade(label=label, menu=submenu)
                
                # Process submenu items
                for subchild in child:
                    if subchild.tag == "Command":
                        label = subchild.attrib.get('label', '')
                        cmd = subchild.attrib.get('command', '')
                        if cmd in handlers:
                            submenu.add_command(label=label, command=handlers[cmd])
                        else:
                            submenu.add_command(label=label)
                    elif subchild.tag == "Separator":
                        submenu.add_separator()
            elif child.tag == "Command":
                # Regular menu command
                label = child.attrib.get('label', '')
                cmd = child.attrib.get('command', '')
                if cmd in handlers:
                    widget.add_command(label=label, command=handlers[cmd])
                else:
                    widget.add_command(label=label)
            elif child.tag == "Separator":
                widget.add_separator()
                
        return widget
    elif tag == "Statusbar":
        widget = ttk.Label(parent, **kwargs)
        widget.pack(side=tk.BOTTOM, fill=tk.X)
        return widget
    elif tag == "Frame":
        if 'text' in kwargs:
            kwargs.pop('text')
            # Frames shouldn't have labels or text

        widget = ttk.Frame(parent, **kwargs)
    else:
        # Default widget creation
        try:
            widget = widget_class(parent, **kwargs)
        except tk.TclError as e:
            if "unknown option" in str(e) and 'text' in kwargs:
                # If widget doesn't support 'text' option, create a label instead
                text = kwargs.pop('text')
                widget = widget_class(parent, **kwargs)
                label = ttk.Label(parent, text=text)
                label.pack(side=tk.LEFT, padx=5)
            else:
                raise
    
    # Store widget ID for later reference
    widget_id = attrs.get('id')
    if widget_id:
        id_registry[widget_id] = widget

    # Handle ID assignment
    if 'id' in element.attrib:
        id_registry[element.attrib['id']] = widget

    # Handle events and text configuration
    if 'action' in element.attrib and isinstance(widget, ttk.Button):
        handler_name = element.attrib['action']
        if handler_name in handlers:
            widget.config(command=handlers[handler_name])
    
    # Handle text attributes for different widget types
    if 'text' in element.attrib and hasattr(widget, 'config') and 'text' in widget.config():
        widget.config(text=element.attrib['text'])
    elif 'label' in element.attrib and hasattr(widget, 'config') and 'label' in widget.config():
        widget.config(label=element.attrib['label'])
    elif hasattr(widget, 'set') and ('text' in element.attrib or 'label' in element.attrib):
        widget.set(element.attrib.get('text') or element.attrib.get('label'))

    # Handle notebook tabs - if parent is a notebook, add as a tab
    if isinstance(parent, ttk.Notebook) and 'text' in element.attrib:
        parent.add(widget, text=element.attrib['text'])
        # Don't pack notebook tabs - they're managed by the notebook
        pack_widget = False
    else:
        pack_widget = not isinstance(widget, tk.Menu)  # Don't pack menus

    # Only pack if needed
    if pack_widget:
        widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Recursively create children with the current widget as parent
    for child in element:
        create_widget(child, widget, handlers)

    return widget

def build_ui(xml_string, handlers):
    # Parse the XML
    root_element = ET.fromstring(xml_string)
    
    # Create the root window
    if root_element.tag == "Window":
        title = root_element.get('title', 'EUIL App')
        width = int(root_element.get('width', 800))
        height = int(root_element.get('height', 600))
        
        root = tk.Tk()
        root.title(title)
        root.geometry(f"{width}x{height}")
        
        # Set application style
        style = ttk.Style()
        style.theme_use('clam')  # More modern look
        
        # Configure styles
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
        
        # Create the main container
        container = ttk.Frame(root)
        container.pack(fill=tk.BOTH, expand=True)
        
        # First pass: Create menu if it exists
        menu_widget = None
        for child in root_element:
            if child.tag == "Menu":
                menu_widget = create_widget(child, root, handlers)
                if menu_widget:
                    root.config(menu=menu_widget)
                break  # Only process one menu
        
        # Second pass: Process all other widgets
        for child in root_element:
            if child.tag == "Menu":
                continue  # Skip menu as it's already processed
                
            widget = create_widget(child, container, handlers)
            if widget and widget != container:  # Don't pack the container itself
                if hasattr(container, 'grid_config'):
                    # Handle grid layout
                    grid = container.grid_config
                    widget.grid(
                        row=grid['row'], 
                        column=grid['col'], 
                        padx=grid['columnspacing']//2, 
                        pady=grid['rowspacing']//2,
                        sticky='nsew'
                    )
                    
                    # Update grid position
                    grid['col'] += 1
                    if grid['col'] >= grid['columns']:
                        grid['col'] = 0
                        grid['row'] += 1
                else:
                    # Default pack layout for other widgets
                    widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure grid weights
        if hasattr(container, 'grid_config'):
            for i in range(container.grid_config['columns']):
                container.columnconfigure(i, weight=1)
            for i in range(container.grid_config['row'] + 1):
                container.rowconfigure(i, weight=1)
        
        return root
    else:
        raise ValueError("Root element must be a Window")
