# coding: utf-8
"""
About - Metadata for Setuptools
"""

# Python 2.7 Standard Library
import importlib
import inspect
import os
import re
import sys

# Third-Party Libraries
import setuptools

# Metadata
__project__ = "about"
__author__  = u"Sébastien Boisgérault <Sebastien.Boisgerault@gmail.com>"
__version__ = "0.3.0"
__license__ = "MIT License"


# The `get_metadata` method mixes responsabilities here, the fact that it 
# handles path issues is madness. The only argument should probably be a
# module object, or maybe a dict. The only responsabilities of get_metadata 
# is too "unmangle" the double underscores (with some cleanup, convergence
# if needed, but really) and to transform the values when the metadata 
# name is known.

# Q: should I try to get all double underscore names (maybe exclude some
#    of the generated such as __file__) ? And transform the values only
#    of the ones I know ? And provide some "hooks" to transform new
#    variables ? I don't know if it makes sense. Remember that the
#    metadata are used to fill the setup function arguments, no less, 
#    no more ... So the answer is no, stick to what we do expect.
#    Should I be more explicit about that and call the function
#    GET_SETUP_KWARGS or something ?

# Can we really confuse the module/package name and the project name ?
# It can still be overloaded after the metadata request, but still ...
# Yeah, it's pretty standard.

# To summarize the purpose of about:
#
#   - provide setup.py with metadata that is already declared: 
#     get rid of the metadata duplication
#     
#   - metadata should be accessible "as usual" from the "__" symbols 
#     in the module, without about being a dependency of this process.
#
#   - provide a command-line tool to display the list of metadata that
#     has been declared and what is missing ...
#

# Rk: as we have concluded that the metadata cannot in general live in the
#     module source code, why not use a data file instead of a module ?
#     Because it would make the insertion of the metadata harder in the
#     module ? Yes, that's right ... We would require some helpers installed
#     at runtime ... Unless we can rely on PEP345 supporting tools ?
#




def get_metadata(name, path=None):
    """
    Return metadata for setuptools `setup`.
    """

    if path is None:
        path = os.getcwd()
    sys.path.insert(0, path)
    about_data = importlib.import_module(name).__dict__
    if path is not None:
        del sys.path[0]
    metadata = {}

    # Q: accept "url" **OR** "home page" ?

    # read the relevant __*__ module attributes
    for name in "project name author version license doc url classifiers".split():
        value = about_data.get("__" + name + "__")
        if value is not None:
            metadata[name] = value

    # when "project" is here, it overrides the (generated) "name" attribute
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

def printer(line, stdin):
    print line,

class About(setuptools.Command):

    description = "Display Project Metadata"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        metadata = self.distribution.metadata

        attrs = [
            ("name"     , metadata.name       ),
            ("version"  , metadata.version    ),
            ("summary"  , metadata.description),
            ("home page", metadata.url        ),
            ("license"  , metadata.license    ),
        ]

        author = metadata.author
        maintainer = metadata.maintainer
        if author:
            attrs.extend([
                ("author", metadata.author      ),
                ("e-mail", metadata.author_email),
            ])
        if maintainer and maintainer != author:
            attrs.extend([
                ("maintainer", metadata.maintainer      ),
                ("e-mail"    , metadata.maintainer_email),
            ])

        desc = metadata.long_description
        if desc:
           line_count = len(desc)
           attrs.append(("description", "yes ({0} lines)".format(line_count)))
        else:
           attrs.append(("description", None))

        attrs.extend([
            ("classifiers" , metadata.classifiers     ),
            ("platform"    , metadata.platforms       ),
            ("download url", metadata.download_url    ),
        ])

        # I am ditching "keywords" but keeping "classifiers".
        # (no one is declaring or using "keywords" AFAICT)
        attrs.append(("classifiers", metadata.classifiers))

        # Get the mandatory, runtime, declarative dependencies 
        # (managed by setuptools).
        attrs.append(("requires", self.distribution.install_requires))

        print
        for name, value in attrs:
            print "  - " + name + ":",
            if isinstance(value, list):
                print
                for item in value:
                  print "      - " + str(item)
            elif isinstance(value, basestring):
                lines = value.splitlines()
                if len(lines) <= 1:
                    print value
                else:
                    print
                    for line in lines:
                        print "      | " + line
            else:
                print "undefined"
        print


if __name__ == "__main__":
    import about
    local = open("about.py", "w")
    local.write(open(inspect.getsourcefile(about)).read())
    local.close()
    
