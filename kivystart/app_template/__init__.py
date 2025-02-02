"""
Module containing the App Template class.
"""
import os

from abc import ABC, abstractmethod
from typing import Optional, List

from kivystart.utils.base import joinpaths
from kivystart.storage import kivystart_storage
from kivystart.renderer import KivyTemplateRenderer


class AppTemplateError(Exception):
    """
    Raised on app template errors.
    """

class Step(ABC):
    """
    Class representing a step/action in project creation.
    """
    def __init__(self, app_template, update: bool = False):
        """
        Initialize a Step instance.
        
        Args:
            app_template (BaseAppTemplate): The app template instance
            update (bool): Condition to update an existing project for the specified fields
        """
        assert isinstance(app_template, BaseAppTemplate), "The app_template argument should be an instance of BaseAppTemplate"
        self.app_template = app_template
        self.update = update
        
    @abstractmethod
    def action(self):
        """
        An action to complete or execute.
        """

class BaseAppTemplate(ABC):
    def __init__(
        self,
        projectname: str,
        appname: str,
        owner_name: Optional[str] = None,
        owner_email: Optional[str] = None,
        no_buildozer: bool = False,
        no_kivymd: bool = False,
        package_name: Optional[str] = None,
        python_version: str = "3.11",
        no_venv: bool = False,
        dependencies: List[str] = [],
        theme: Optional[str] = None,
        default_screen: Optional[str] = None,
        git_init: bool = False,
        license: Optional[str] = None,
        kivy_version: Optional[str] = None,
   ):
        """
        Initializes the base template with parameters for directory structure, project, and app name.
        """
        self.projectname = projectname
        self.appname = appname
        self.owner_name = owner_name
        self.owner_email = owner_email
        self.no_buildozer = no_buildozer
        self.no_kivymd = no_kivymd
        self.package_name = package_name
        self.python_version = python_version
        self.no_venv = no_venv
        self.dependencies = dependencies
        self.theme = theme
        self.default_screen = default_screen
        self.git_init = git_init
        self.license = license
        self.kivy_version = kivy_version
    
    @abstractmethod
    def create_project(self, destination_dir: str, update: bool = False):
        """
        Create the project structure in the provided directory.
        
        Args:
            destination_dir (str): The destination directory to put the project into
            update (bool): Condition to update an existing project for the specified fields
        """


class KivyMDAppTemplate(BaseAppTemplate):
    # Basic app template with only KivyMD support
    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         if self.no_kivymd:
            raise AppTemplateError("KivyMD only app template. Argument 'no_kivymd' must be set to False")
