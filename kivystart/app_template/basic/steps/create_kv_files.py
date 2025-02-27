"""
Create kv files step
"""
import os
import pathlib

from kivystart.app_template import Step
from kivystart.renderer import KivyTemplateRenderer
from kivystart.utils.base import (
    joinpaths,
    click_echo,
    recursive_get_files,
)

# Initialize template renderer
TemplateRenderer = KivyTemplateRenderer()


class CreateKvFilesStep(Step):
    def create_kv_files(self):
        """
        Create the kv_files
        """
        kv_files_source_dir = joinpaths(self.app_template.source_dir, "kv_files")
        files = recursive_get_files(kv_files_source_dir, "*.kivytemplate")
        global_context = {
            "appname": self.app_template.appname,
        }
        
        TemplateRenderer.set_context(global_context)
        
        for file in files:
            relative_file = pathlib.Path(file).relative_to(self.app_template.source_dir)
            relative_file = str(relative_file).split('.kivytemplate', 1)[0]
            
            with open(file, "r") as fd:
                content = TemplateRenderer.render(fd.read())
                self.app_template.save_file(relative_file, content, mode="w" if self.update else "x")
        
    def action(self):
        # Main entry point
        kv_files_destination = joinpaths(self.app_template.destination_dir, "kv_files")
        
        # Create kv_files
        if self.app_template.appname:
            self.create_kv_files()
            click_echo("Successfully created kv_files!", fg="cyan")
        else:
            click_echo("Skipping kv_files creation, App name not provided", fg="yellow")
        