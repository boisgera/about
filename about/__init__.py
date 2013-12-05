
# Python 2.7 Standard Library
import importlib
import re
import sys

# Metadata
from .__about__ import *

# TODO:
#
#   - think of distribution of about. Should it be embedable into every project
#     for simplicity ? in a "utils" directory for example ? 
#
#   - use cases:
#
#       - The project is Pure Python with no dependency beyond the standard library.
#         The metadata can be embedded into the main module which can be imopted and
#         introspected. In this case, exec is optional, but is there any pb in
#         keeping it ? "__name__" is not going to get added automatically, it has
#         to be set manually into the source file. That's about it ? Manually
#         setting it can be a problem, for example if the module is also an 
#         executable. So it should not be done ...
#         Make the user set the name explicitely. Arf that sucks. The other option
#         is to define __name__ in a fallback clause ... Nah, won't work, in an
#         exec, __name__ would be defined (as __builtin__). We could argue that
#         we are talking project name, not module/script name and go for another
#         name than __name__ ? That's probably the right thing to do.
#      
#       - Pure Python project with dependencies. Make a package out of it and
#         have an __about__.py file at the top-level, that is without dependency
#         this file is exec'd in setup.py and its contents imported in the module.
#         We HAVE to do that: in setup.py, we can't import unless the top-level
#         package does not have extra dependcy, and in the module, once deployed,
#         we rely on the module import machinery to file the file ...
#         WAIT. We could always rely on import, if we set the path to the top-level
#         package and import from there. It bypasses the package __init__.py.
#         Yes, that should always work ... 
#
#         Apart from the __name__ issue, that means that for the import to work,
#         the __*__ field have to be set in __all__ for the "import *" to work.
#         This is not mandatory of course, this stuff can be imported explicitely
#         one by one. 

# TODO: signature to (module/package) name, path ?
def get_metadata(name, path=None):
    """
    Return metadata for setuptools `setup`.
    """

    if path is not None:
        sys.path.insert(0, path)
    metadata = importlib.import_module(name).__dict__
    if path is not None:
        del sys.path[0]

    # read the relevant __*__ module attributes
    for name in "project author version license doc url classifiers".split():
        value = about_data.get("__" + name + "__")
        if value is not None:
            metadata[name] = value

    # get the project name
    project = metadata.get("project")
    if project is not None:
        metadata["name"] = project
        del metadata["project"]

    # search for author email with <...@...> syntax in the author field
    author = metadata.get("author")
    if author is not None:
        email_pattern = r"<([^>]+@[^>]+)>"
        match = re.search(email_pattern, author)
        if match is not None:
            metadata["author_email"] = email = match.groups()[0]
            metadata["author"] = author.replace("<" + email + ">", "").strip()

    # get the module short description from the docstring
    doc = metadata.get("doc")
    if doc is not None:
        lines = [line for line in doc.splitlines() if line.strip()]
        metadata["description"] = lines[0].strip()
        del metadata["doc"]

    # process trove classifiers
    classifiers = metadata.get("classifiers")
    if classifiers and isinstance(classifiers, str):
        classifiers = [l.strip() for l in classifiers.splitlines() if l.strip()]
        metadata["classifiers"] = classifiers

    return metadata


