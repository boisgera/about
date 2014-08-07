#!/usr/bin/env python

# Python 2.7 Standard Library
import os
import sys

# Third-Party Libraries
try:
    import setuptools
except ImportError:
    error  = "pip is not installed, "
    error += "refer to <http://www.pip-installer.org> for instructions."
    raise ImportError(error)

# Local Libraries
sys.path.insert(0, "lib")
import .about

metadata = about.get_metadata(about)
contents = dict(py_modules=["about"], zip_safe=False)
requirements = dict(install_requires=["path.py", "setuptools", "sh"]) 
plugins = dict(entry_points={"distutils.commands": "about = about:About"})

info = {}
info.update(contents)
info.update(metadata)
info.update(requirements)
info.update(plugins)

if __name__ == "__main__":
    setuptools.setup(**info)

