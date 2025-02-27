#!/usr/bin/env python
"""
Module for creating project structures for a kivy project.
"""
import re
import os
import click
import time

from typing import Optional, List

from kivystart.commands import (
    MakeProjectCommand, MakeProjectError,
)
from kivystart.licenses import LICENSES
from kivystart.ansi import art
from kivystart.utils.base import click_echo


@click.group(invoke_without_command=True)
@click.option('-V', '--version', is_flag=True, help="Show the version and exit.")
@click.pass_context
def cli(ctx, version):
    """
    KivyStart CLI - Manage your projects with ease.
    """
    # Add current directory to python path
    if not version:
        click_echo(art, prefix="", fg="red", bold=True)
        click_echo("🚀 KivyStart - Your Dynamic Kivy Project Generator 🚀", prefix="", bold=True, fg="red")
        click_echo("\n", prefix="")
    if version:
        # Show the version
        click.echo(kivystart_version)
    elif not ctx.invoked_subcommand:
        # Print usage if no subcommands are invoked
        click_echo(ctx.get_help(), prefix="")


@cli.command()
@click.argument("name")
@click.argument("appname")
@click.option('-O', '--owner', default=None, help="The owner of the kivy project in format 'Fullname <email@something.com>' ")
@click.option('-nb', '--no-buildozer', is_flag=True, default=False, help="Condition on whether to create a buildozer file. Defaults to False.")
@click.option('-U', '--update', is_flag=True, default=False, help="This updates an existing project with new data. This will recreate dynamic files and create static files if they don't exist.")
@click.option('-nmd', "--no-kivymd", is_flag=True, default=False, help="Add this flag if you want strictly the Kivy version of the project (removing KivyMD support).")
@click.option('-t', '--template', default='basic', type=click.Choice(["basic", "navigation", "game"]), help="The template for the project (e.g., 'basic', 'navigation', 'game'). Some templates will be coming soon.")
@click.option('-pkg', '--package-name', default=None, help="The package name for the project (e.g., 'com.example.myapp').")
@click.option('-py', '--python-version', default='3.9', help="The Python version to use in the project (e.g., '3.10').")
@click.option('-nv', '--no-venv', is_flag=True, default=False, help="Skip creation of a virtual environment.")
@click.option('-r', '--dependencies', default='', help="Comma-separated list of additional dependencies to include in requirements.txt(e.g., 'requests,sqlite3').")
@click.option('-m', '--theme', default=None, help="The theme for the project (e.g., 'dark', 'light').")
@click.option('-s', '--default-screen', default=None, help="Create a predefined screen (e.g., 'login', 'home', 'settings'). Coming soon.")
@click.option('-git', '--git-init', is_flag=True, default=False, help="Initialize a Git repository for the project.")
@click.option('-l', '--license', default=None, help=f"Add a LICENSE file with the specified license. Available options are {tuple(LICENSES.keys())}.")
@click.option('-kv', "--kivy-version", default=None, help="Minimum kivy version supported")
def makeproject(
    name: str,
    appname: str,
    owner: Optional[str],
    no_buildozer: bool,
    update: bool,
    no_kivymd: bool,
    template: str,
    package_name: Optional[str],
    python_version: str,
    no_venv: bool,
    dependencies: str,
    theme: Optional[str],
    default_screen: Optional[str],
    git_init: bool,
    license: Optional[str],
    kivy_version: Optional[str],
):
    """
    Creates a Kivy startup project.
    
    WARNING: If the --update flag is True, to surely protect your files from being overwritten, make sure you
    move them somewhere or make a backups or change conflicting files/directories.
    
    Args:
        name: The project name.
       appname: The name of the application usually ending with a suffix 'App' eg DemoApp.
    """
    # Do some validation first.
    
    owner_name, owner_email = None, None
    dependencies = (dependencies.split(',') if dependencies else []) or []
    
    if not appname.endswith("App"):
        raise MakeProjectError("The appname does not follow standard recommendations. App name must have a suffix 'App' e.g. (DemoApp)")
    
    if owner:
        owner_regex = re.compile(r"^[A-Za-z\s]+ <[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+>$")
        if not owner_regex.fullmatch(owner):
            raise MakeProjectError("The owner flag value must be in format 'Fullname <email>' ")
        
        owner_name, owner_email = owner.split('<', 1)
        owner_name, owner_email = owner_name.strip(), owner_email.strip(">").strip()
    
    kivy = "Kivy" if no_kivymd else "KivyMD"
    click_echo(f"Creating your {kivy} Project!", fg="red", bold=True)
        
    time.sleep(1)
    
    click_echo("I'm going to f*ck up your project 😤\n", fg="red", bold=True)
    time.sleep(2)
    
    click_echo("Kidding, I'm going to create an awesome project 😇 ", fg="green", bold=True)
    time.sleep(1.5)
    
    click_echo("Thanks to my creator @digreatbrian 🌟💫\n", fg="green", bold=True)
    time.sleep(1.5)
    
    # Call the make project logic
    MakeProjectCommand.main(
        name = name,
        appname = appname,
        owner_name = owner_name,
        owner_email = owner_email,
        no_buildozer = no_buildozer,
        update = update,
        no_kivymd = no_kivymd,
        template = template or "basic",
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


if __name__ == "__main__":
    cli()