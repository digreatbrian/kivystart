"""
Basic App Template
"""
import os
import click
import time
import sys
import pathlib
import webbrowser
import subprocess

from typing import Dict

from kivystart.app_template import (
    BaseAppTemplate,
    AppTemplateError,
    Step,
)
from kivystart.licenses import get_license_heading_and_body
from kivystart.utils.base import (
    joinpaths,
    expand_exception,
    click_echo,
)
from kivystart.utils.dateutils import gmt_date
from kivystart.storage import kivystart_storage
from kivystart.renderer import KivyTemplateRenderer
from kivystart.app_template.basic.steps import (
    CreateAssetsStep,
    CreateComponentsStep,
    CreateControllersStep,
    CreateCodeOwnersStep,
    CreateKvFilesStep,
    CreateModelsAndUtilsStep,
    FinalTouchesStep,
)
from kivystart.version import __version__
from kivystart.buildozer import update_buildozer_spec


# Initialize template renderer
TemplateRenderer = KivyTemplateRenderer()


class CreateRootFilesStep(Step):
    def create_license(self, license_heading, license_body):
        """
        Create a LICENSE file.
        """
        template_content = ""
        template = joinpaths(self.app_template.source_dir, "LICENSE.kivytemplate")
        
        with open(template, "r") as fd:
            template_content = fd.read()
        
        # render license template
        TemplateRenderer.set_context({
            "fullname": self.app_template.owner_name or "<Your Fullname here>",
            "license_heading": license_heading or "<License Heading here>",
            "license_body": license_body or "<License Body here>",
        })
        
        # Render template
        content = TemplateRenderer.render(template_content)
        
        # Save the LICENSE file
        mode = "x" if not self.update else "w"
        self.app_template.save_file("LICENSE", content=content, mode=mode)
        
    def create_readme(self,):
        """
        Create README.md file
        """
        readme_content = ""
        readme = joinpaths(self.app_template.source_dir, "README.md")
        
        with open(readme, "r") as fd:
            readme_content = fd.read()
            
        # No need for rendering this readme
        # Save the LICENSE file
        mode = "x" if not self.update else "w"
        self.app_template.save_file("README.md", content=readme_content, mode=mode)
        
    def create_main_py(self,):
        """
        Create main.py file
        """
        main_py_content = ""
        template = joinpaths(self.app_template.source_dir, "main.py.kivytemplate")
        
        with open(template, "r") as fd:
            main_py_content = fd.read()
        
        # render main.py template
        TemplateRenderer.set_context({
            "kivystart_version": __version__,
            "owner_name": self.app_template.owner_name,
            "owner_email": self.app_template.owner_email,
            "appname": self.app_template.appname,
            "kivy_version": self.app_template.kivy_version,
            "owner_email": self.app_template.owner_email,
            "projectname": self.app_template.projectname,
            "creation_date": gmt_date(),
        })
        
        # Render template
        content = TemplateRenderer.render(main_py_content)
        
        mode = "x" if not self.update else "w"
        self.app_template.save_file("main.py", content=content, mode=mode)
    
    def create_buildozer_spec(self):
        """
        Create a buildozer.spec file
        """
        cmd = ["buildozer", "init"]
        subprocess.run(cmd, check=True)
    
    def apply_buildozer_spec_patches(self) -> Dict:
        """
        Updates the buildozer.spec file with the provided fields
        
        Returns:
            Dict: The updated fields
        """
        buildozer_spec_path = joinpaths(self.app_template.destination_dir, "buildozer.spec")
        fields = {
            "title": self.app_template.appname.rstrip("App"),
            "requirements": "python3,kivy"
        }
        
        if self.app_template.package_name:
            fields["package.name"] = self.app_template.package_name
        
        if self.app_template.kivy_version:
            fields["osx.kivy_version"] = self.app_template.kivy_version
        
        if self.app_template.owner_name:
            fields["author"] = f"© {self.app_template.owner_name}"
        
        if self.app_template.python_version:
            fields["osx.python_version"] = self.app_template.python_version.split('.', 1)[0]
        
        if self.app_template.no_kivymd:
            fields["requirements"] += ",kivymd"
        
        if self.app_template.dependencies:
            fields["requirements"] += "," + ",".join(self.app_template.dependencies)
        
        content = update_buildozer_spec(buildozer_spec_path, fields, strict_fields=["title"])
        mode = "w"
               
        # Save new buildozer.spec file
        self.app_template.save_file("buildozer.spec", content, mode=mode)
        return fields
        
    def create_requirements_txt(self):
        """
        Create requirements.txt file
        """
        requirements_content = ""
        template = joinpaths(self.app_template.source_dir, "requirements.txt.kivytemplate")
        
        with open(template, "r") as fd:
            requirements_content = fd.read()
        
        # render requirements.txt template
        TemplateRenderer.set_context({
            "dependencies": "\n".join(self.app_template.dependencies)
        })
        
        # Render template
        content = TemplateRenderer.render(requirements_content)
        
        mode = "x" if not self.update else "w"
        self.app_template.save_file("requirements.txt", content=content, mode=mode)
    
    def create_theme_py(self):
        """
        Create theme.py file
        """
        theme_content = ""
        template = joinpaths(self.app_template.source_dir, "theme.py.kivytemplate")
        
        with open(template, "r") as fd:
            theme_content = fd.read()
        
        # render theme.py template
        TemplateRenderer.set_context({
            "theme": self.app_template.theme,
        })
        
        # Render template
        content = TemplateRenderer.render(theme_content)
        
        mode = "x" if not self.update else "w"
        self.app_template.save_file("theme.py", content=content, mode=mode)
        
    def action(self):
        """
        Action to create project root files.
        """
        # files -> LICENSE, README, main.py, buildozer.spec
        
        # Create LICENSE
        if self.app_template.license:
            license_heading, license_body = get_license_heading_and_body(self.app_template.license)
            self.create_license(license_heading, license_body)
            click_echo("Created LICENSE successfully!", fg="cyan")
        else:
            click_echo("Skipped LICENSE creation, no license specified", fg="yellow")
        
        # Create README.md
        readme_fullpath = joinpaths(self.app_template.destination_dir, "README.md")
        if not os.path.isfile(readme_fullpath):
            self.create_readme()
            click_echo("Created README.md successfully!", fg="cyan")
        else:
            click_echo("Skipped README.md creation, already exists", fg="yellow")
        
        # Create main.py
        if self.app_template.appname:
            self.create_main_py()
            click_echo("Successfully created main.py!", fg="cyan")
        else:
            click_echo("Skipping main.py creation, App name not provided", fg="yellow")
        
        # Create buildozer spec
        if not self.app_template.no_buildozer:
            buildozer_success = False
            try:
                popen = subprocess.run(["buildozer"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if not os.path.isfile(joinpaths(self.app_template.destination_dir, "buildozer.spec")):
                    self.create_buildozer_spec()
                    click_echo("Successfully created buildozer.spec!", fg="cyan")
                else:
                    click_echo("Skipped buildozer init, buildozer.spec exists", fg="yellow")
                
                buildozer_success = True
            except FileNotFoundError:
                # buildozer not installed
                click_echo("Skipping buildozer.spec creation, buildozer is not installed.", fg="yellow")
            
            if buildozer_success:
                try:
                    click_echo("Applying buildozer.spec patches", fg="cyan")
                    fields = self.apply_buildozer_spec_patches()
                    click_echo(f"Applied patches to fields: {list(fields.keys())}", fg="cyan")
                    click_echo("Make sure to do a review on the buildozer.spec", fg="cyan")
                except FileNotFoundError:
                    click_echo("Skipping patches, buildozer spec file not found", fg="yellow")
        else:
            click_echo("Skipping buildozer.spec creation, no_buildozer flag is enabled.", fg="yellow")
        
        # Create requirements.txt file
        requirements_fullpath = joinpaths(self.app_template.destination_dir, "requirements.txt")
        if not os.path.isfile(requirements_fullpath) or self.app_template.dependencies:
            self.create_requirements_txt()
            click_echo("Created requirements.txt successfully!", fg="cyan")
        else:
            if os.path.isfile(requirements_fullpath):
                click_echo("Skipped requirements.txt creation, already exists", fg="yellow")
            else:
                click_echo("Skipped requirements.txt creation, no dependencies specified", fg="yellow")
        
        # Create theme.py
        self.create_theme_py()
        click_echo("Created theme.py successfully!", fg="cyan")


class BasicAppTemplate(BaseAppTemplate):
    # Basic app template with Kivy + KivyMD support 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.theme and self.theme not in ["dark", "light"]:
            raise AppTemplateError(f"Theme '{self.theme}' not supported for this app template, available themes: ['dark', 'light']")
        
    @property
    def source_dir(self) -> str:
        """
        Returns the source/base directory for fetching project templates
        """
        if self.no_kivymd:
            return joinpaths(kivystart_storage, "templates/basic/kivy")
        else:
            return joinpaths(kivystart_storage, "templates/basic/kivymd")
        
    def save_file(self, filepath: str, content: str, mode: str = "x", makedirs: bool = True):
        """
        Saves a file in the current app template destination_dir under the provided filepath.
        
        Args:
            filepath (str): The filepath of file, provide only filepath if you want to save file in root directory of the destination_dir.
            content (str): The content to save in final file.
            mode (str): Mode for saving file. Defaults to 'x' for saving file if only it doesn't exist.
            makedirs (bool): Whether to create directories if they don't exist.
        """
        final_file_fullpath = pathlib.Path(joinpaths(self.destination_dir, filepath))
        final_file_dir = final_file_fullpath.parent
        
        if makedirs:
            # create directories
            os.makedirs(str(final_file_dir), exist_ok=True)
         
        try:
             with open(final_file_fullpath, mode) as fd:
                 fd.write(content)
        except FileExistsError:
             raise AppTemplateError(f"Cannot save file, it seems like file '{filepath}' already exists. Try to use --update flag to bypass this.")
             
    def create_project(self, destination_dir: str, update):
        """
        Create the project structure in the provided directory.
        
        Args:
            destination_dir (str): The destination directory to put the project into
            update (bool): Condition to update an existing project for the specified fields
         """
        self.destination_dir = destination_dir
        steps = [
            CreateRootFilesStep(self, update=update),
            CreateAssetsStep(self, update=update),
            CreateComponentsStep(self, update=update),
            CreateControllersStep(self, update=update),
            CreateCodeOwnersStep(self, update=update),
            CreateKvFilesStep(self, update=update),
            CreateModelsAndUtilsStep(self, update=update),
            FinalTouchesStep(self, update=update)
        ] # steps to execute arranged in order at this point
        
        for step in steps:
            try:
                if steps.index(step) == len(steps) - 1:
                    # Last step
                    click_echo("Doing some touchups, get ready 🚖", fg="cyan", bold=True)
                    step.action() # Execute the step.
                    click_echo(f"Completed and finalized the final step '{step.__class__.__name__}'\n", fg="green", bold=True)
                    
                    time.sleep(1.5)
                    click_echo("I'm done with your sh*t, it's time to thank my creater🥳", fg="yellow", bold=True)
                    time.sleep(2)
                    
                    click_echo("For converting your kivy app to APK 👨‍💻 use my creator's github action at https://github.com/digreatbrian/buildozer-action", fg="yellow", bold=True)
                    
                    click_echo("I'm redirecting you to support my creator✨", fg="yellow", bold=True)
                    choice = input(click.style("\nConfirm (y/N): ", fg="yellow", bold=True))
                    click.echo("")
                    if choice.lower().startswith("y"):
                        if self.owner_name:
                            click_echo("Nice choice %s! ✅"%self.owner_name.split(' ', 1)[0], fg="green", bold=True)
                        else:
                            click_echo("Yoo, you are very awesome! 😍", fg="green", bold=True)
                        
                        time.sleep(1)
                        click_echo("Going to https://ko-fi.com/digreatbrian", fg="yellow", bold=True)
                        
                        time.sleep(1)
                        opened = webbrowser.open_new("https://ko-fi.com/digreatbrian")
                        
                        if not opened:
                            print("")
                            click_echo("Failed to open browser! 😔", fg="red", bold=True)
                            click_echo("Please continue to https://ko-fi.com/digreatbrian", fg="yellow", bold=True)
                            
                    else:
                       if self.owner_name:
                            click_echo("One of the worst decisions, I'm going to f*ck up your projects next tym  %s! 😡"%self.owner_name.split(' ', 1)[0], fg="red", bold=True)
                       else:
                            click_echo("Bad choice, I'm going to f*ck up your projects next tym! 😡", fg="red", bold=True)

                else:
                    step.action() # Execute the step.
                    click_echo(f"Completed and finalized step '{step.__class__.__name__}'\n", fg="green", bold=True)
            except Exception as e:
                expanded_exc = expand_exception(e)
                click_echo(expanded_exc, prefix="")
                click_echo(f"Error executing step '{step.__class__.__name__}', template: 'basic'\n{e}", fg="red", bold=True)
                
                if steps.index(step) == 0:
                    # Exit immediately as first step failed.
                    sys.exit()
