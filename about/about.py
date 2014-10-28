# coding: utf-8

metadata = dict(
  __name__        = "about",
  __version__     = "4.0.1-alpha.5",
  __license__     = "MIT License",  
  __author__      = u"Sébastien Boisgérault <Sebastien.Boisgerault@gmail.com>",
  __url__         = "https://warehouse.python.org/project/about",
  __summary__     = "Software Metadata for Humans",
  __readme__      = "README.md",
  __classifiers__ = ["Programming Language :: Python :: 2.7" ,
                     "Topic :: Software Development"         ,
                     "Operating System :: OS Independent"    ,
                     "Intended Audience :: Developers"       ,
                     "License :: OSI Approved :: MIT License",
                     "Development Status :: 3 - Alpha"       ]
)

globals().update(metadata)

__all__ = metadata.keys()
