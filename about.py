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
from path import path
import pkg_resources
import setuptools
import sh


#
# Metadata
# ------------------------------------------------------------------------------
#
__all__  = ["get_metadata"]
__main__ = (__name__ == "__main__") # we are about to override __name__.

metadata = dict(
    __name__        = "about",
    __version__     = "4.0.0-alpha",
    __license__     = "MIT License",
    __author__      = u"Sébastien Boisgérault <Sebastien.Boisgerault@gmail.com>",
    __url__         = "https://warehouse.python.org/project/about",
    __summary__     = "Software Metadata for Humans",
    __readme__      = None,
    __doc__         = __doc__,
    __classifiers__ = ["Programming Language :: Python :: 2.7" ,
                       "Topic :: Software Development"         ,
                       "Operating System :: OS Independent"    ,
                       "Intended Audience :: Developers"       ,
                       "License :: OSI Approved :: MIT License",
                       "Development Status :: 3 - Alpha"       ]
)

globals().update(metadata)

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
            REST = trueish(parser.get("global", "rest"))
        except ConfigParser.NoOptionError:
            pass
    return REST

def trueish(value):
    if not isinstance(value, str):
        return bool(value)
    else:
        value = string.lower(value)
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
    build_rest = rest_generation_required()
    if readme is not None:
        readme_rst = readme + ".rst"
        if build_rest:
            try:
                _ = sh.pandoc
            except sh.CommandNotFound:
                error = "cannot find pandoc to generate ReST documentation."
                raise ImportError(error)
            sh.pandoc("-o", readme_rst, readme) 
        
        if os.path.exists(readme_rst):
            readme_filename = readme_rst
        else:
            readme_filename = readme
        setuptools_kwargs["long_description"] = open(readme_filename).read()
 
    # Process trove classifiers.
    classifiers = metadata.get("__classifiers__")
    if classifiers and isinstance(classifiers, str):
        classifiers = [c.strip() for c in classifiers.splitlines() if c.strip()]
    setuptools_kwargs["classifiers"] = classifiers

    return setuptools_kwargs


# Get rid of this ? Is this information not already in the PKG-INFO file ?
class About(setuptools.Command):

    description = "Display Project Metadata"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        metadata = self.distribution.metadata

        attrs = [
            ("name"     , metadata.name       ),
            ("version"  , metadata.version    ),
            ("summary"  , metadata.description),
            ("homepage" , metadata.url        ),
            ("license"  , metadata.license    ),
        ]

        author = metadata.author
        maintainer = metadata.maintainer
        if author:
            attrs.extend([
                ("author", metadata.author      ),
                ("e-mail", metadata.author_email),
            ])
        if maintainer and maintainer != author:
            attrs.extend([
                ("maintainer", metadata.maintainer      ),
                ("e-mail"    , metadata.maintainer_email),
            ])

        desc = metadata.long_description
        if desc:
           line_count = len(desc)
           attrs.append(("description", "yes ({0} lines)".format(line_count)))
        else:
           attrs.append(("description", None))

        attrs.extend([
            # I am ditching "keywords" but keeping "classifiers".
            # (no one is declaring or using "keywords" AFAICT)
            ("classifiers" , metadata.classifiers     ),
            # How can we specify the platforms in the setup.py ?
            ("platforms"   , metadata.platforms       ),
            # Do we need a download url ?
            ("download url", metadata.download_url    ),
        ])

        # Get the mandatory, runtime, declarative dependencies 
        # (managed by setuptools).
        attrs.append(("requires", self.distribution.install_requires))

        print
        for name, value in attrs:
            print "  - " + name + ":",
            if isinstance(value, list):
                print
                for item in value:
                  print "      - " + str(item)
            elif isinstance(value, basestring):
                lines = value.splitlines()
                if len(lines) <= 1:
                    print value
                else:
                    print
                    for line in lines:
                        print "      | " + line
            else:
                print "undefined"
        print


if __main__:
    import about # this, my dear, is buggy if about exist locally.
    local = open("about.py", "w")
    local.write(open(inspect.getsourcefile(about)).read())
    local.close()

