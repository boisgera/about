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
sys.path.insert(0, local(".lib"))
setup_requires = ["about>=5"]
for req in setup_requires:
    try:
        require = lambda *r: pkg_resources.WorkingSet().require(*r)
        require(req)

    except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
        error = """{req!r} not found; install it locally with:

    pip install --target=.lib --ignore-installed {req!r}"""
        raise ImportError(error.format(req=req))
import about

# ------------------------------------------------------------------------------

sys.path.insert(0, local("about"))
import about
import about.about

info = dict(
  metadata     = about.get_metadata(about.about),
  contents     = {
                   "package_data": {"":  ["*.txt"]},
                   "packages": setuptools.find_packages()
                 },
  requirements = {"install_requires": ["setuptools"]}, 
  scripts      = {},
  plugins      = {},
  tests        = {},
)

if __name__ == "__main__":
    kwargs = {k:v for dct in info.values() for (k,v) in dct.items()}
    setuptools.setup(**kwargs)

