"""
BoloDocs User Interface Module

Contains Streamlit-based UI components for document interaction.
"""

from .app import main  # Explicitly expose the main entry point

__all__ = ["main"]  # Controls what's exposed via `from interface import *`
__version__ = "1.0.0"  # Track UI version separately