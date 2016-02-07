
About
================================================================================

**Summary:** define the metadata of your project in a single place, 
then make it available at setup-time and at runtime.

Let's consider the `about` package as an example ; we add to our project
files, in the source tree, a file named `about.py` that contains the metadata 
of the project:


    about
    |--- setup.py
    |--- README.md
    |...
    |--- about
    |    |--- __init__.py
    |    |...
    |    |--- about.py

This file contains the metadata (and a little boilerplate):

    # coding: utf-8

    metadata = dict(
      __name__        = "about",
      __version__     = "5.0.0-alpha",
      __license__     = "MIT License",  
      __author__      = u"Sébastien Boisgérault <Sebastien.Boisgerault@gmail.com>",
      __url__         = "https://warehouse.python.org/project/about",
      __summary__     = "Software Metadata for Humans",
      __keywords__    = "python/2.7, OS independent, software development, alpha",
    )

    globals().update(metadata)
    __all__ = metadata.keys()

**Setup.** To use this metadata, the `setup.py` file includes the code:

    import about
    import about.about

    info = about.get_metadata(about.about)

    # add extra information (contents, requirements, etc.).
    info.update(...)

    if __name__ == "__main__":
        setuptools.setup(**info)

**Runtime.** The metadata is stored as a collection of attributes of the 
`about.about` module. If we include in the `about/__init__.py` file the 
one-liner
    
    from .about import *

they become available in the top-level module:

    >>> import about
    >>> print about.__name__
    about
    >>> print about.__version__
    4.0.0
    >>> print about.__license__
    MIT License


