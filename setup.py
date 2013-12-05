#!/usr/bin/env python

# Python 2.7 Standard Library
import os
# Third-Party Libraries
import setuptools
import about


metadata = about.get_metadata("about", path=os.getcwd())
contents = dict(py_modules=["about"], zip_safe=False)
requirements = {}

info = {}
info.update(contents)
info.update(metadata)
info.update(requirements)

if __name__ == "__main__":
    setuptools.setup(**info)

