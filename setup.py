#!/usr/bin/env python

# Python 2.7 Standard Library
import os
import sys

# Third-Party Libraries
try:
    import setuptools
except ImportError:
    error = "pip is not installed, refer to <{url}> for instructions."
    raise ImportError(error.format(url="http://pip.readthedocs.org"))

# Local Libraries
sys.path.insert(0, "lib")
import about

metadata     = about.get_metadata(about)
contents     = dict(py_modules=["about"], zip_safe=False)
requirements = dict(install_requires=["path.py", "setuptools", "sh"]) 
data         = dict(data_files = [("", ["README.md"])])
plugins      = dict(entry_points={"distutils.commands": "about = about:About"})

info = {}
info.update(metadata)
info.update(contents)
info.update(requirements)
info.update(plugins)

if __name__ == "__main__":
    setuptools.setup(**info)

