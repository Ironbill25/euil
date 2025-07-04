"""
EUIL - Extensible UI Language

A simple XML-based UI library for Tkinter applications.
"""

__version__ = "0.1.0"

from .core import build_ui, create_widget, id_registry
from .main import main as cli_main

__all__ = [
    'build_ui',
    'create_widget',
    'id_registry',
    'cli_main'
]