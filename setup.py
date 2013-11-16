#!/usr/bin/env python

# Python 2.7 Standard Library
pass

# Third-Party Libraries
import setuptools
import about

# ------------------------------------------------------------------------------
metadata = about.get_metadata("about/__about__.py")

contents = dict(packages=["about"], zip_safe=True)

requirements = {}

# ------------------------------------------------------------------------------
info = {}
info.update(contents)
info.update(metadata)
info.update(requirements)

setuptools.setup(**info)

