"""
Create assets directory step.
"""
import os
import shutil

from kivystart.app_template import Step
from kivystart.utils.base import joinpaths, click_echo


class CreateAssetsStep(Step):
    def create_assets(self):
        """
        Create assets directory
        """
        # Create empty assets directory and sub directories
        assets_destination = joinpaths(self.app_template.destination_dir, "assets")
        
        fonts = joinpaths(assets_destination, "fonts")
        images = joinpaths(assets_destination, "images")
        
        os.makedirs(fonts, exist_ok=True)
        os.makedirs(images, exist_ok=True)
    
    def action(self):
        # Main entry point
        assets_destination = joinpaths(self.app_template.destination_dir, "assets")
        if os.path.isdir(assets_destination):
            click_echo("Skipping assets creation, assets directory already exists", fg="yellow")
        else:
            self.create_assets()
            click_echo("Created assets directory successfully!", fg="cyan")
