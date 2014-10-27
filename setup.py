#!/usr/bin/env python

# Python 2.7 Standard Library
import ConfigParser
import os
import os.path
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


# Setup Libraries 
# ------------------------------------------------------------------------------
def trueish(value):
    if not isinstance(value, str):
        return bool(value)
    else:
        value = value.lower()
        if value in ("y", "yes", "t", "true", "on", "1"):
            return True
        elif value in ("", "n", "no", "f", "false", "off", "0"):
            return False
        else:
            raise TypeError("invalid bool value {0!r}, use 'true' or 'false'.")

setuptools.Distribution.global_options.append(
  ("lib", "l", "install setup dependencies")
)

def lib_required():
    LIB = False
    if "-l" in sys.argv:
        sys.argv.remove("-l")
        LIB = True
    elif "--lib" in sys.argv:
        sys.argv.remove("--lib")
        LIB = True
    elif os.path.isfile("setup.cfg"):
        parser = ConfigParser.RawConfigParser()
        parser.read("setup.cfg")
        try: 
            LIB = trueish(parser.get("global", "lib"))
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            pass
    return LIB

def install_lib(setup_requires, libdir="lib"):
    # TODO: remove pyc files ? (no cross-platform ?)
    shutil.rmtree(libdir)
    os.mkdir(libdir)
    pip_install = pip.commands["install"]().main
    for package in setup_requires:
        options = ["--quiet", "--target=" + libdir, "--ignore-installed"]
        error = pip_install(options + [package])
        if error:
            raise RuntimeError("failed to install {0}.".format(package))
    os.chmod(libdir, 0o777)
    for dir, subdirs, others in os.walk(libdir):
        files = [os.path.join(dir, file) for file in subdirs + others]
        for file in files:
            os.chmod(file , 0o777)
    assert sys.path[0] in ("", os.getcwd())
    sys.path.insert(1, libdir)

if lib_required():
    install_lib(setup_requires)

# ------------------------------------------------------------------------------

import about

metadata     = about.get_metadata(about)
contents     = dict(packages = setuptools.find_packages())
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

