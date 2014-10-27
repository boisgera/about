#!/usr/bin/env python
# coding: utf-8

# Python 2.7 Standard Library
import ConfigParser
import importlib
import inspect
import os.path
import pydoc
import re
import sys
import types

# Third-Party Libraries
import pkg_resources
import setuptools
import sh

#
# Metadata
# ------------------------------------------------------------------------------
#
__main__ = (__name__ == "__main__") # we are about to override __name__.

from .about import *

#
# Setuptools Monkey-Patching
# ------------------------------------------------------------------------------
#
setuptools.Distribution.global_options.append(
  ("rest", "r", "generate ReST README")
)

#
# ReStructuredText Generation Support
# ------------------------------------------------------------------------------
#
def rest_generation_required():
    # We sort of assume here that we are being called from a setup.py.
    # To be safe, we should CHECK that in get_metadata and generate
    # an error otherwise.
    REST = False
    if "-r" in sys.argv:
        sys.argv.remove("-r")
        REST = True
    elif "--rest" in sys.argv:
        sys.argv.remove("--rest")
        REST = True
    elif os.path.isfile("setup.cfg"):
        parser = ConfigParser.RawConfigParser()
        parser.read("setup.cfg")
        try: 
            REST = trueish(parser.get("about", "rest"))
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            pass
    return REST

def generate_rest_readme(filename):
    readme = filename
    readme_rst = filename + ".rst"
    try:
        _ = sh.pandoc
    except sh.CommandNotFound:
        error = "cannot find pandoc to generate ReST documentation."
        raise ImportError(error)
    sh.pandoc("-o", readme_rst, readme) 

def trueish(value):
    if not isinstance(value, str):
        return bool(value)
    else:
        value = value.lower()
        if value in ("y", "yes", "t", "true", "on", "1"):
            return True
        elif value in ("", "n", "no", "f", "false", "off", "0"):
            return False
        else:
            raise TypeError("invalid bool value {0!r}, use 'true' or 'false'.")

#
# Generation of Metadata for Setuptools
# ------------------------------------------------------------------------------
#
def get_metadata(source):
    """
    Extract the metadata from the module or dict argument.

    It returns a `metadata` dictionary that provides keywords arguments
    for the setuptools `setup` function.
    """
    if isinstance(source, types.ModuleType):
        metadata = source.__dict__
    else:
        metadata = source

    setuptools_kwargs = {}

    for key in "name version url license".split():
        val = metadata.get("__" + key + "__")
        if val is not None:
            setuptools_kwargs[key] = val

    version = metadata.get("__version__")
    if version is not None:
        setuptools_kwargs["version"] = version

    # Search for author email with a <...@...> syntax in the author field.
    author = metadata.get("__author__")
    if author is not None:
        author = author.encode("utf-8")
        email_pattern = r"<([^>]+@[^>]+)>"
        match = re.search(email_pattern, author)
        if match is not None:
            setuptools_kwargs["author_email"] = email = match.groups()[0]
            setuptools_kwargs["author"] = author.replace("<" + email + ">", "").strip()
        else:
            setuptools_kwargs["author"] = author

    # Get the module summary.
    summary = metadata.get("__summary__")
    if summary is not None:
        setuptools_kwargs["description"] = summary

    # Get and process the module README, 
    # under the assumption that `__readme__` is the name of a markdown file.
    readme = metadata.get("__readme__")
    if readme is not None:
        if rest_generation_required():
            generate_rest_readme(filename=readme)
        if os.path.exists(readme + ".rst"):
            setuptools_kwargs["long_description"] = open(readme + ".rst").read()
 
    # Process trove classifiers.
    classifiers = metadata.get("__classifiers__")
    if classifiers and isinstance(classifiers, str):
        classifiers = [c.strip() for c in classifiers.splitlines() if c.strip()]
    setuptools_kwargs["classifiers"] = classifiers

    return setuptools_kwargs

