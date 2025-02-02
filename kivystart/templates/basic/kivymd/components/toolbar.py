"""
MainToolbar - A navigation bar or action bar placed typically at the top of the screen. 
It contains buttons for user actions or navigation. The toolbar is a sibling to the MainContainer and is located above it in the layout hierarchy.
"""

import pathlib

from kivy.lang import Builder
from kivymd.uix.toolbar import MDTopAppBar


# Define the path to the KV file
app_dir = pathlib.Path(__file__).resolve().parent.parent
kv_path = app_dir / "kv_files" / "main_toolbar.kv"


# Load the KV file without reassigning MainContainer
with open(str(kv_path), encoding="utf-8") as kv_file:
    Builder.load_string(kv_file.read())


class MainToolbar(MDTopAppBar):
    pass  # Do not overwrite this class
