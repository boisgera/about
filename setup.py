#!/usr/bin/env python

# Python 2.7 Standard Library
import ConfigParser
import os
import os.path
import shutil
import sys

# Pip Package Manager
try:
    import pip
    import setuptools
    import pkg_resources
except ImportError:
    error = "pip is not installed, refer to <{url}> for instructions."
    raise ImportError(error.format(url="http://pip.readthedocs.org"))

def local(path):
    return os.path.join(os.path.dirname(__file__), path)

# Extra Third-Party Libraries
try:
    setup_requires = ["sh"]
    require = lambda *r: pkg_resources.WorkingSet().require(*r)
    require(*setup_requires)
    import about
except pkg_resources.DistributionNotFound:
    error = """{req!r} not found; install it locally with:

    pip install --target=.lib --ignore-installed {req!r}
"""
    raise ImportError(error.format(req=" ".join(setup_requires)))
sys.path.insert(1, local(".lib"))
import sh


# ------------------------------------------------------------------------------

import about
import about.about

info = dict(
  metadata     = about.get_metadata(about.about),
  code         = dict(packages = setuptools.find_packages()),
  data         = dict(data_files = [("", ["README.md"])]),
  requirements = dict(install_requires=["setuptools", "sh"]), 
  scripts      = {},
  plugins      = {},
  tests        = {},
)



if __name__ == "__main__":
    kwargs = {k:v for dct in info.values() for (k,v) in dct.items()}
    setuptools.setup(**kwargs)

