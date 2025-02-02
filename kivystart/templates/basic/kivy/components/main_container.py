"""
MainContainer holds the core content of the app. This could include widgets 
like labels, buttons, and other UI elements. It is the first descendant of 
MainScreen and is the area where most of the interactive elements reside.
"""

import pathlib

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


# Define the path to the KV file
app_dir = pathlib.Path(__file__).resolve().parent.parent
kv_path = app_dir / "kv_files" / "main_container.kv"


# Load the KV file without reassigning MainContainer
with open(str(kv_path), encoding="utf-8") as kv_file:
    Builder.load_string(kv_file.read())


class MainContainer(BoxLayout):
    pass  # Do not overwrite this class
