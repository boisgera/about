#!/usr/bin/env python

# Python 2.7 Standard Library
pass

# Third-Party Libraries
import about
import setuptools

metadata = about.get_metadata("about/__about__.py")

contents = {"packages": setuptools.find_packages()}

requirements = {}

info = {}
info.update(contents)
info.update(metadata)
info.update(requirements)


setuptools.setup(**info)

