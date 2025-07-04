"""
EUIL Feature Demo

This example demonstrates various features of the EUIL library.
"""
from tkinter import messagebox
from euil import build_ui

def on_submit():
    name = id_registry.get('name_entry').get()
    if name:
        messagebox.showinfo("Greeting", f"Hello, {name}!")
    else:
        messagebox.showwarning("Warning", "Please enter your name")

def on_checkbox_changed():
    checked = id_registry['dark_mode_var'].get()
    style = 'clam' if checked else 'default'
    root = id_registry.get('root_window')
    style = ttk.Style(root)
    style.theme_use(style)

# UI Definition
XML = """
<Window title="EUIL Feature Demo" width="600" height="400" id="root_window">
    <Notebook>
        <Frame text="Form">
            <Grid columns="2" padding="10" spacing="5">
                <Label text="Name:" />
                <Entry id="name_entry" />
                
                <Label text="Age:" />
                <Spin from="1" to="120" />
                
                <Label text="Country:" />
                <Combo values="USA,Canada,UK,Germany,France,Japan" />
                
                <Frame />
                <Check text="Dark Mode" id="dark_mode_var" command="on_checkbox_changed" />
                
                <Button text="Submit" action="on_submit" colspan="2" />
            </Grid>
        </Frame>
        
        <Frame text="About">
            <Frame padding="20">
                <Label text="EUIL Demo" font="Arial 16 bold" />
                <Label text="A simple XML-based UI library for Tkinter" />
                <Separator />
                <Text id="about_text" height="10" width="50">
                    This is a demonstration of EUIL's features.
                    You can create complex UIs with simple XML syntax.
                </Text>
            </Frame>
        </Frame>
    </Notebook>
</Window>
"""

if __name__ == "__main__":
    import ttkbootstrap as ttk
    from euil import id_registry
    
    handlers = {
        'on_submit': on_submit,
        'on_checkbox_changed': on_checkbox_changed
    }
    
    root = build_ui(XML, handlers)
    root.mainloop()
