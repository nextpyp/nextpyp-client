
# configuration file for Sphinx documentation, see:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Example config for making it actually look good:
# https://github.com/JamesALeedham/Sphinx-Autosummary-Recursion

# Docstring documentation
#   cross references:
#       https://www.sphinx-doc.org/en/master/usage/referencing.html
#   Python roles:
#       https://www.sphinx-doc.org/en/master/usage/domains/python.html#python-roles


# load local extensions
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '_ext'))

# project info
project = 'nextpyp-client'
author = 'Jeff Martin'

# general sphinx config
extensions = [

    # generate docs from code automatically
    # https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
    'sphinx.ext.autodoc',

    # generate index pages from code automatically
    # https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html
    'sphinx.ext.autosummary',

    # better than the built-in autodoc_typehints = 'description' option
    # https://github.com/tox-dev/sphinx-autodoc-typehints
    'sphinx_autodoc_typehints',

    # allow saner docstring formats
    # https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
    # that are actually documented somewhere!
    # https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard
    'sphinx.ext.napoleon',

    # custom extension to allow additional RST markup
    'rst_roles'
]
templates_path = ['_templates']

# styling
html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_css_files = ['style.css']

# autosummary config
# https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html#generating-stub-pages-automatically
autosummary_generate = True

# autodoc config
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration
autoclass_content = "class"  # only show the class docstring with the class, not __init__ too
autodoc_class_signature = 'separated'  # show the __init__ method separately from the class itself
autodoc_typehints = 'description'  # write the type hints in the <thing> descriptions, rather than the signature

# sphinx_autodoc_typehints config
# https://github.com/tox-dev/sphinx-autodoc-typehints#options
# NOTE: don't turn this on, it duplicates method params
# always_document_param_types = True
typehints_defaults = 'comma'

# napoleon config
napoleon_numpy_docstring = True
napoleon_google_docstring = False
napoleon_attr_annotations = True
