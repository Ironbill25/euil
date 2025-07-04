import tkinter as tk
from .. import EUIL

# Example handlers
def submit_form():
    name = EUIL.id_registry.get('nameEntry').get()
    email = EUIL.id_registry.get('emailEntry').get()
    age = EUIL.id_registry.get('ageSpin').get()
    country = EUIL.id_registry.get('countryCombo').get()
    
    status = EUIL.id_registry.get('statusBar')
    if status:
        status.config(text=f"Submitted: {name}, {age} from {country}")
    
    print(f"Form submitted: {name}, {email}, {age}, {country}")

def start_progress():
    progress = EUIL.id_registry.get('progressBar')
    if progress:
        progress.start(10)
        progress.after(3000, lambda: progress.stop())

def update_volume(value):
    text = EUIL.id_registry.get('volumeText')
    if text:
        text.config(text=f"Volume: {int(float(value))}%")

# Menu command handlers
def new_file():
    text = EUIL.id_registry.get('textEditor')
    if text:
        text.delete('1.0', tk.END)

def open_file():
    print("Open file dialog would appear here")

def save_file():
    text = EUIL.id_registry.get('textEditor')
    if text:
        content = text.get('1.0', tk.END)
        print(f"Saving content: {content[:50]}...")

def exit_app():
    root.quit()

def cut_text():
    text = EUIL.id_registry.get('textEditor')
    if text:
        text.event_generate('<<Cut>>')

def copy_text():
    text = EUIL.id_registry.get('textEditor')
    if text:
        text.event_generate('<<Copy>>')

def paste_text():
    text = EUIL.id_registry.get('textEditor')
    if text:
        text.event_generate('<<Paste>>')

# Run the UI
if __name__ == "__main__":
    try:
        with open("example.euil", "r") as f:
            xml_ui = f.read()
        
        # Register all handlers
        handlers = {
            'submit_form': submit_form,
            'start_progress': start_progress,
            'new_file': new_file,
            'open_file': open_file,
            'save_file': save_file,
            'exit_app': exit_app,
            'cut_text': cut_text,
            'copy_text': copy_text,
            'paste_text': paste_text
        }
        
        # Build and run the UI
        root = EUIL.build_ui(xml_ui, handlers)
        
        # Set up volume scale callback
        volume_scale = EUIL.id_registry.get('volumeScale')
        if volume_scale:
            volume_scale.config(command=update_volume)
            volume_scale.set(50)  # Default volume
        
        # Set initial status
        status = EUIL.id_registry.get('statusBar')
        if status:
            status.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Start the main loop
        root.mainloop()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()