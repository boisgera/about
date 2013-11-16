# encoding: utf-8
"""
About - Metadata for Setuptools
"""

__name__    = "about"
__author__  = u"Sébastien Boisgérault <Sebastien.Boisgerault@gmail.com>"
__version__ = "0.0.1-alpha.2"
__license__ = "MIT License"

export = "doc author version license".split()
__all__ = ["__" + name + "__" for name in export]
