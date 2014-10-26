About - Metadata for Setuptools

Define the metadata of your project in a single place, then make it
available in the setup and at runtime.

The standard pattern, for a simple module `myproject`, is to define an
extra metadata module `about_myproject`:

    # about_myproject.py
    """
    My Project Summary

    My Project Long Description
    """

    metadata = dict(
        __appname__     = "myproject",
        __version__     = "1.0.0",
        __license__     = "MIT License",
        __author__      = u"Sébastien Boisgérault <Sebastien.Boisgerault@gmail.com>",
        __url__         = "https://warehouse.python.org/project/about",
        __doc__         = __doc__,
        __docformat__   = "markdown",
        __classifiers__ = ["Programming Language :: Python :: 2.7",
                           "Topic :: Software Development",
                           "License :: OSI Approved :: MIT License"]
      )

    globals().update(metadata)
    __all__ = metadata.keys()

Then, in `myproject.py`, you add a metadata section

    # Metadata
    from .about_myproject import *

and finally, in your `setup.py` file, use the following code:

    import setuptools
    import about
    import .about_myproject

    info = about.get_metadata(about_myproject)

    # add extra information (contents, requirements, etc.) for the setup.
    info.update(...)

    if __name__ == "__main__":
        setuptools.setup(**info)
