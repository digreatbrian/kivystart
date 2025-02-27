"""
Commands for the KivyStart CLI
"""
import os

from typing import Optional, List

from kivystart.storage import kivystart_storage
from kivystart.utils.dateutils import gmt_date
from kivystart.utils.base import joinpaths
from kivystart.app_template.basic import BasicAppTemplate


class MakeProjectError(Exception):
    """
    Raised on exceptions encountered whilst executing makeproject command.
    """
    

class MakeProjectCommand:
    # makeproject command
    templates = {"basic": BasicAppTemplate}
    
    @classmethod
    def setup(cls):
        # Setups before command execution
        pass
    
    @classmethod
    def main(
        cls,
        name: str,
        appname: str,
        owner_name: Optional[str] = None,
        owner_email: Optional[str] = None,
        no_buildozer: bool = False,
        update: bool = False,
        no_kivymd: bool = False,
        template: str = 'basic',
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
        cls.setup()
        cls.makeproject(
            name = name,
            appname = appname,
            owner_name = owner_name,
            owner_email = owner_email,
            no_buildozer = no_buildozer,
            update = update,
            no_kivymd = no_kivymd,
            template = template,
            package_name = package_name,
            python_version = python_version,
            no_venv = no_venv,
            dependencies = dependencies,
            theme = theme,
            default_screen = default_screen,
            git_init = git_init,
            license = license,
            kivy_version = kivy_version,
        )
    
    @classmethod     
    def makeproject(
        cls,
        name: str,
        appname: str,
        owner_name: Optional[str] = None,
        owner_email: Optional[str] = None,
        no_buildozer: bool = False,
        update: bool = False,
        no_kivymd: bool = False,
        template: str = 'basic',
        package_name: Optional[str] = None,
        python_version: str = "3.11",
        no_venv: bool = False,
        dependencies: List[str] = [],
        theme: Optional[str] = None,
        default_screen: Optional[str] = None,
        git_init: bool = False,
        license: Optional[str] = None,
        kivy_version: Optional[str] = None
    ):
        """
        Execute makeproject after all setups and pre-command actions.
        """
        app_template_cls = cls.templates.get(template)
        
        if not app_template_cls:
            raise MakeProjectError(f"App template '{template}' not supported, possible templates are {tuple(cls.templates.keys())}")
        
        app_template = app_template_cls(
            projectname = name,
            appname = appname,
            owner_name = owner_name,
            owner_email = owner_email,
            no_buildozer = no_buildozer,
            no_kivymd = no_kivymd,
            package_name = package_name,
            python_version = python_version,
            no_venv = no_venv,
            dependencies = dependencies,
            theme = theme,
            default_screen = default_screen,
            git_init = git_init,
            license = license,
            kivy_version = kivy_version,
        )
        base_dir = joinpaths(os.path.abspath('.'), name)
        app_template.create_project(base_dir, update=update)
