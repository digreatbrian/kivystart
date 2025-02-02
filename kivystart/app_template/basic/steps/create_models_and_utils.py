"""
Create utils and models directories step.
"""
import os
import pathlib

from kivystart.app_template import Step
from kivystart.utils.base import joinpaths, click_echo, recursive_get_files


class CreateModelsAndUtilsStep(Step):
    def create_models(self):
        """
        Create the models directory
        """
        models_source_dir = joinpaths(self.app_template.source_dir, "models")
        files = recursive_get_files(models_source_dir, "*.py")
        
        for file in files:
            relative_file = pathlib.Path(file).relative_to(self.app_template.source_dir)
            
            with open(file, "r", encoding="utf-8", errors="ignore") as fd:
                content = fd.read()
            
            self.app_template.save_file(
                str(relative_file),
                content,
                mode="w" if self.update else "x")
                
    def create_utils(self):
        """
        Create the utils directory
        """
        utils_source_dir = joinpaths(self.app_template.source_dir, "utils")
        files = recursive_get_files(utils_source_dir, "*.py")
        
        for file in files:
            relative_file = pathlib.Path(file).relative_to(self.app_template.source_dir)
            
            with open(file, "r", encoding='utf-8') as fd:
                content = fd.read()
            
            self.app_template.save_file(
                str(relative_file),
                content,
                mode="w" if self.update else "x")
        
    def action(self):
        # Main entry point
        
        self.create_models()
        click_echo("Created models directory successfully!", fg="cyan")
        
        self.create_utils()
        click_echo("Created utils directory successfully!", fg="cyan")
