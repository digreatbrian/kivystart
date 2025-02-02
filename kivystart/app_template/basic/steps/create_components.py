"""
Create components step
"""
import os
import pathlib

from kivystart.app_template import Step
from kivystart.utils.base import (
    joinpaths,
    click_echo,
    recursive_get_files,
)


class CreateComponentsStep(Step):
    def create_components(self):
        """
        Create the components
        """
        components_source_dir = joinpaths(self.app_template.source_dir, "components")
        files = recursive_get_files(components_source_dir)
        
        for file in files:
            relative_file = pathlib.Path(file).relative_to(self.app_template.source_dir)
            with open(file, "r") as fd:
                self.app_template.save_file(str(relative_file), fd.read(), mode="w" if self.update else "x")
        
    def action(self):
        # Main entry point
        components_destination = joinpaths(self.app_template.destination_dir, "components")
        if os.path.isdir(components_destination):
            if not self.update:
                click_echo("Skipping components creation, components directory already exists and --update flag is not provided", fg="yellow")
            else:
                self.create_components()
                click_echo("Created and merged components directory successfully!", fg="cyan")
        else:
            self.create_components()
            click_echo("Created components directory successfully!", fg="cyan")
