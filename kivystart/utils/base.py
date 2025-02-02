"""
Utilities and helpers module.
"""
import os
import click
import fnmatch
import traceback

from typing import List


def joinpaths(path1: str, path2: str, *more):
    """
    Returns joined paths but makes sure all paths are included in the final path rather than os.path.join
    """
    path1 = path1.rstrip("/")
    path2 = path2.lstrip("/")  # clean paths
    finalpath = os.path.join(path1, path2)

    for p in more:
        finalpath = finalpath.rstrip("/")
        p = p.lstrip("/")
        finalpath = os.path.join(finalpath, p)
    return finalpath


def expand_exception(e: Exception) -> str:
    """
    Expands an exception to show the traceback and more information.

    Args:
        e (Exception): The exception to expand.

    Returns:
        str: The expanded exception.
    """
    return "".join(
        traceback.format_exception(type(e), value=e, tb=e.__traceback__))


def click_echo(data: str, prefix: str = "* ", **kwargs):
    """
    Function using click.echo for writing messages to the console.
    
    Args:
        data (str): String to print to console
        prefix (str): Prefix to add to message before printing.
        **kwargs: Keyword arguments for styling to parse to click.style
    """
    click.echo(click.style(prefix + data, **kwargs))


def recursive_get_files(path, pattern="*") -> List[str]:
    """Recursively collect files which matches a certain pattern"""
    if os.path.isfile(path):
        if fnmatch.fnmatch(path, pattern):
            return [path]
        return []
    
    elif os.path.isdir(path):
        all_files = []
        for root, _, files in os.walk(path):
            for file in files:
                if fnmatch.fnmatch(file, pattern):
                    all_files.append(joinpaths(root, file))
        return all_files
    else:
        raise FileNotFoundError("The provided path is neither an existing file nor directory.")
