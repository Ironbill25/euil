"""
Tests for the EUIL package.
"""
import sys
import os
import pytest
import tkinter as tk

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from euil import build_ui, id_registry

class TestEUIL:
    def test_basic_window_creation(self):
        """Test creating a basic window."""
        xml = """
        <Window title="Test Window">
            <Label text="Hello, EUIL!" />
        </Window>
        """
        root = build_ui(xml, {})
        assert isinstance(root, tk.Tk)
        root.destroy()

    def test_widget_creation(self):
        """Test creating various widgets."""
        xml = """
        <Window>
            <Frame id="main_frame">
                <Button id="test_button" text="Click me" />
                <Entry id="test_entry" />
            </Frame>
        </Window>
        """
        root = build_ui(xml, {})
        
        # Check if widgets were created and stored in the registry
        assert 'main_frame' in id_registry
        assert 'test_button' in id_registry
        assert 'test_entry' in id_registry
        
        # Check widget types
        from tkinter import ttk
        assert isinstance(id_registry['test_button'], ttk.Button)
        assert isinstance(id_registry['test_entry'], ttk.Entry)
        
        root.destroy()

    def test_event_handling(self):
        """Test event handling."""
        clicked = [False]
        
        def on_click():
            clicked[0] = True
        
        xml = """
        <Window>
            <Button id="btn" text="Click" action="on_click" />
        </Window>
        """
        
        root = build_ui(xml, {'on_click': on_click})
        
        # Simulate button click
        id_registry['btn'].invoke()
        
        assert clicked[0] is True
        root.destroy()