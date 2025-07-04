"""
Simple EUIL Application Example
"""
from euil import build_ui

def on_button_click():
    print("Button was clicked!")

# Define the UI in XML
XML = """
<Window title="Simple EUIL App" width="300" height="200">
    <Frame padding="10">
        <Label text="Welcome to EUIL!" font="Arial 12 bold" />
        <Button text="Click Me!" action="on_button_click" padding="10" />
    </Frame>
</Window>
"""

if __name__ == "__main__":
    handlers = {
        'on_button_click': on_button_click
    }
    root = build_ui(XML, handlers)
    root.mainloop()
