
# Python 2.7 Standard Library
import re

# Metadata
from .__about__ import *

def get_metadata(filename):
    """
    Return metadata for setuptools `setup`.
    """

    file = open(filename).read()
    about_data = {}
    exec file in {}, about_data

    metadata = {}

    # read the relevant __*__ module attributes
    for name in "name author version license doc url classifiers".split():
        value = about_data.get("__" + name + "__")
        if value is not None:
            metadata[name] = value

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


