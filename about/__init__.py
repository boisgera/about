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

#
# Metadata
# ------------------------------------------------------------------------------
#
__main__ = (__name__ == "__main__") # we are about to override __name__.

from .about import *

#
# ReStructuredText Generation Support
# ------------------------------------------------------------------------------
#

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

#
# Generation of Metadata for Setuptools
# ------------------------------------------------------------------------------
#

TROVE = pkg_resources.resource_string("about", "Trove-classifiers.txt")

# TODO: preprocess TROVE a list of lists of words (split on "::" and space and /)
#       Mmmm that's probably not very smart. Consider a split on "::" only probably.
#       Arf: "/" has a special meaning: most of the time (always ?), it is a OR,
#       (or AND depending on your POV: a group of several related categories)
#       or a synonym ; matching one of the component of the / should be a 100%. 
#       Arf this is a mess; not only do we have things like "OS/2" that don't fit
#       but sometimes A B / C should be read as (A B) / (A C), not (A B) / C.
#       I may need to annotate (use quotes and braces for example ?) the list
#       of classifiers for an easier processsing. 
# TODO. given a keywords, split in words. 
#       Then, should compare with the list of lists, weight according to
#       fragment match, weigh with the "specialisation" of the match ...
#       Matching is the end is better than matching the start, BUT, this
#       is sometimes ambiguous, sometimes not, and that semantic info is
#       NOT in the list, I definitely NEED to decorate it. Ex: we cannot
#       be satisfied with only "appplication" that matches ...
#
#       finally, try https://pypi.python.org/pypi/python-Levenshtein/0.12.0 ?
#       or be strict at the fragment level ? Nah, work out something simpler.
#
#       Try on the real list to think of all sequence of word that would be
#       good enough. THEN, think of a method. 

def trove_search(keyword):
    results = []
    for classifier in TROVE:
        value = difflib.SequenceMatcher(None, keyword, classifier).ratio() 
        results.append((value, classifier))
    return sorted(results)

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


    # TODO: grab the alpha/beta/production status from the version.
    # TODO: grab the license info from the license.
    # TODO: grap the keywords ("," separated or list ?) and best-match vs trove list
    #       after case normalization. Should we fuzzy-match ? Always find the best ?
    #       Ignore the unclear ? use difflib ? (http://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/). Yeahn use fuzzy wuzzy to get the best match for some
# string and the corresponding score ... or optionally a list of the best matches.
# Externalize this particular feature ?
    #       How are we supposed to specify some hierarchy, e.g. Turbogears :: Applications ?
    #       Drop the "::" in the string ?
    # TODO: finally, use the classifiers if any.
    classifiers = []

    keywords = metadata.get("__keywords__")

    classifiers = metadata.get("__classifiers__")
    if classifiers and isinstance(classifiers, str):
        classifiers = [c.strip() for c in classifiers.splitlines() if c.strip()]
    setuptools_kwargs["classifiers"] = classifiers

    return setuptools_kwargs

