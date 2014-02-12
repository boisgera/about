#!/usr/bin/env python

# Python 2.7 Standard Library
import os

# Third-Party Libraries
import setuptools
import about


metadata = about.get_metadata("about", path=os.getcwd())
contents = dict(py_modules=["about"], zip_safe=False)
requirements = dict(install_requires="setuptools") 
plugins = dict(entry_points={"distutils.commands": "about = about:About"})

info = {}
info.update(contents)
info.update(metadata)
info.update(requirements)
info.update(plugins)

if __name__ == "__main__":
    setuptools.setup(**info)

