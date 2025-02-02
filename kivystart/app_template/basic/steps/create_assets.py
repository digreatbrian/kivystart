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
        assets_destination = joinpaths(self.app_template.destination_dir, "assets")
        assets_source = joinpaths(self.app_template.source_dir, "assets")
        shutil.copytree(assets_source, assets_destination) 
    
    def action(self):
        # Main entry point
        assets_destination = joinpaths(self.app_template.destination_dir, "assets")
        if os.path.isdir(assets_destination):
            click_echo("Skipping assets creation, assets directory already exists", fg="yellow")
        else:
            self.create_assets()
            click_echo("Created assets directory successfully!", fg="cyan")
