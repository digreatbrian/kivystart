"""
Create CODEOWNERS step
"""
import os
import pathlib

from kivystart.app_template import Step
from kivystart.utils.base import (
    joinpaths,
    click_echo,
    recursive_get_files,
)
from kivystart.renderer import KivyTemplateRenderer


TemplateRenderer = KivyTemplateRenderer()


class CreateCodeOwnersStep(Step):
    def create_codeowners(self):
        """
        Create the CODEOWNERS file
        """
        codeowners_template = joinpaths(self.app_template.source_dir, "docs/CODEOWNERS.kivytemplate")
        template_content = ""
        
        with open(codeowners_template, "r") as fd:
            template_content = fd.read()
        
        # render CODEOWNERS template
        TemplateRenderer.set_context({
            "owner_email": self.app_template.owner_email,
        })
        
        # Render template
        content = TemplateRenderer.render(template_content)
        
        # Save the CODEOWNERS file
        mode = "x" if not self.update else "w"
        self.app_template.save_file("docs/CODEOWNERS", content=content, mode=mode)
        
    def action(self):
        # Main entry point
        codeowners_destination = joinpaths(self.app_template.destination_dir, "docs/CODEOWNERS")
        
        if not self.app_template.owner_email:
            click_echo("Skipping CODEOWNERS creation, owner email not provided", fg="yellow")
        else:
            self.create_codeowners()
            click_echo("Created CODEOWNERS file successfully!", fg="cyan")
