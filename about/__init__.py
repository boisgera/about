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
import difflib
import pkg_resources
import setuptools
import sh

# Metadata
# ------------------------------------------------------------------------------
__main__ = (__name__ == "__main__") # we are about to override __name__.

from .about import *

# ReStructuredText Generation Support
# ------------------------------------------------------------------------------

# Setuptools monkey-patching
setuptools.Distribution.global_options.append(
  ("rest", "r", "generate ReST README")
)

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

# Generation of Metadata for Setuptools
# ------------------------------------------------------------------------------
trove = None

def clean(text):
    text = text.replace("(", "").replace(")", "")
    text = text.replace("/", " ")
    text = text.replace(" - ", " ")
    return text.lower()

def generate_trove():
    global trove
    if trove is None:
        trove = []
        load = pkg_resources.resource_string
        trove_text = load("about", "Trove-classifiers.txt")
        for trove_id in trove_text.splitlines():
            parts = trove_id.split(" :: ")
            context = clean(" ".join(parts[:-1])).split()
            name = clean(parts[-1]).split()
            trove.append({"id": trove_id, "name": name, "context": context})

def match(items, ref_items, trove=trove):
    matches = [item in ref_items for item in items].count(True)
    score = float(matches) / (len(items) + len(ref_items) - matches)
    #print "*", score, items, ref_items
    return score

def trove_search(keyword):
    generate_trove()
    parts = [p.strip().lower() for p in keyword.split("/")]
    try:
        name = parts[-1].split() 
        if len(parts) == 2:
            context = parts[0].split()
        else:
            context = None
    except:
        error = "Invalid keyword {keyword!r}"
        raise ValueError(error.format(keyword=keyword))
    matches = {}
    for item in trove:
        score = match(name, item["name"])
        matches.setdefault(score, []).append(item)
    max_ = sorted(matches.keys())[-1]
    if len(matches[max_]) == 1:
        return matches[max_][0]["id"]
    elif context:
        matches = {}
        subtrove = [matches[max_]]
        for item in subtrove:
            score = match(name, item["context"])
            matches.setdefault(score, []).append(item)
        max_ = sorted(matches.keys())[-1]
        if len(matches[max_]) == 1:
            return matches[max_][0]["id"]

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
 
    # TODO: add license info from license field and dvlpt status from version.
    # Process trove classifiers.
    keywords = metadata.get("__keywords__")
    if keywords is not None:
        classifiers = []
        keywords = [k.strip() for k in keywords.split(",")]
        for keyword in keywords:
            trove_id = trove_search(keyword)
            if trove_id is None:
                error = "ambiguous keyword: {keyword!r}"
                raise ValueError(error.format(keyword=keyword))
            else:
                classifiers.append(trove_id)
        classifiers = sorted(list(set(classifiers)))
        setuptools_kwargs["classifiers"] = classifiers

    return setuptools_kwargs

