"""Command-line interface for EUIL."""

import argparse
import importlib
import sys
from pathlib import Path

def main():
    """Run the EUIL application from command line."""
    parser = argparse.ArgumentParser(description='Run an EUIL application.')
    parser.add_argument('file', help='Path to the .euil file')
    parser.add_argument('--handlers', '-H', help='Python module containing handler functions')
    
    args = parser.parse_args()
    
    # Load the EUIL file
    with open(args.file, 'r', encoding='utf-8') as f:
        xml_string = f.read()
    
    # Load handlers if specified
    handlers = {}
    if args.handlers:
        try:
            # Add the directory containing the handlers to the path
            handlers_path = str(Path(args.handlers).parent)
            if handlers_path not in sys.path:
                sys.path.append(handlers_path)
            
            # Import the module
            module_name = Path(args.handlers).stem
            handlers_module = importlib.import_module(module_name)
            
            # Find all callable objects in the module that don't start with '_'
            for name in dir(handlers_module):
                if not name.startswith('_') and callable(getattr(handlers_module, name)):
                    handlers[name] = getattr(handlers_module, name)
        except Exception as e:
            print(f"Error loading handlers: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Build and run the UI
    from . import build_ui
    root = build_ui(xml_string, handlers)
    root.mainloop()

if __name__ == '__main__':
    main()
