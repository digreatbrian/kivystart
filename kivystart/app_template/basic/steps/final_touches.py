"""
Final touches step
"""

import subprocess

from kivystart.app_template import Step
from kivystart.utils.base import click_echo


class FinalTouchesStep(Step):
    def git_init(self):
        """
        Initialize project as git repository.
        """
        cmd = ["git", "init"]
        subprocess.run(cmd, check=True)
    
    def create_virtual_env(self, python_exe):
        """
        Create a virtual environment
        """
        cmd = [python_exe, "-m", "venv", "venv"]
        subprocess.run(cmd, check=True)
    
    def action(self):
        # Main entry point
        # Initialize git repo
        if self.app_template.git_init:
            try:
                popen = subprocess.run(["git"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.git_init()
                click_echo("Successfully initialized git repository!", fg="cyan")
            except FileNotFoundError:
                # buildozer not installed
                click_echo("Skipping git init, git is not installed.", fg="yellow")
        else:
            click_echo("Skipping git init, git_init flag is not provided.", fg="yellow")
        
        # Create virtual environment
        if not self.app_template.no_venv:
            try:
                python_exe = "python"
                if self.app_template.python_version:
                    python_exe += self.app_template.python_version
                popen = subprocess.run([python_exe, "-m", "venv"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.create_virtual_env(python_exe)
                click_echo("Successfully created virtual environment", fg="cyan")
            except FileNotFoundError:
                # venv not installed
                click_echo("Skipping virtual environment creation, venv is not installed.", fg="yellow")
        else:
            click_echo("Skipping virtual environment creation, no_venv flag is enabled.", fg="yellow")
        
        