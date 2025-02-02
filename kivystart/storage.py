"""
Internal storage helpers module for the KivyStart package.
"""
import os


def kivystart_storage() -> str:
    """
    Return the base directory for the KivyStart package.
    """
    return os.path.abspath(os.path.dirname(__file__))


kivystart_storage = kivystart_storage()
