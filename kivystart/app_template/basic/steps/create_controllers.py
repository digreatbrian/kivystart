"""
Create controllers step
"""
import os
import pathlib

from kivystart.app_template import Step
from kivystart.utils.base import (
    joinpaths,
    click_echo,
    recursive_get_files,
)


class CreateControllersStep(Step):
    def create_controllers(self):
        """
        Create the controllers
        """
        controllers_source_dir = joinpaths(self.app_template.source_dir, "controllers")
        files = recursive_get_files(controllers_source_dir)
        
        for file in files:
            relative_file = pathlib.Path(file).relative_to(self.app_template.source_dir)
            with open(file, "r") as fd:
                self.app_template.save_file(str(relative_file), fd.read(), mode="w" if self.update else "x")
        
    def action(self):
        # Main entry point
        controllers_destination = joinpaths(self.app_template.destination_dir, "controllers")
        if os.path.isdir(controllers_destination):
            if not self.update:
                click_echo("Skipping controllers creation, controllers directory already exists and --update flag is not provided", fg="yellow")
            else:
                self.create_controllers()
                click_echo("Created and merged components directory successfully!", fg="cyan")
        else:
            self.create_controllers()
            click_echo("Created controllers directory successfully!", fg="cyan")
