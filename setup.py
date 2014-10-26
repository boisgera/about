#!/usr/bin/env python

# Python 2.7 Standard Library
import ConfigParser
import os
import shutil
import sys

# Third-Party Libraries
try:
    import pip
    import setuptools
except ImportError:
    error = "pip is not installed, refer to <{url}> for instructions."
    raise ImportError(error.format(url="http://pip.readthedocs.org"))

# Local Libraries
setup_requires = ["sh"]
if not os.path.exists("lib"):
    os.mkdir("lib")
    pip_install = pip.commands["install"]().main
    for package in setup_requires:
        error = pip_install(["--target=lib", "--ignore-installed", package])
        if error:
            raise RuntimeError("failed to install {0}.".format(package))

sys.path.insert(0, "lib")
import about

metadata     = about.get_metadata(about)
contents     = dict(py_modules=["about"], zip_safe=False)
requirements = dict(install_requires=["setuptools", "sh"]) 
data         = dict(data_files = [("", ["README.md"])])
scripts      = {}
plugins      = {}

info = {}
info.update(metadata)
info.update(contents)
info.update(requirements)
info.update(data)
info.update(scripts)
info.update(plugins)

if __name__ == "__main__":
    setuptools.setup(**info)

