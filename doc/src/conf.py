
# configuration file for Sphinx documentation, see:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Example config for making it actually look good:
# https://github.com/JamesALeedham/Sphinx-Autosummary-Recursion


# project info
project = 'nextpyp-client'
author = 'Jeff Martin'

# general sphinx config
extensions = [

    # allow markdown doc files
    # https://myst-parser.readthedocs.io
    'myst_parser',

    # generate docs from code automatically
    # https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
    'sphinx.ext.autodoc',

    # generate index pages from code automatically
    # https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html
    'sphinx.ext.autosummary',

    # better than the built-in autodoc_typehints = 'description' option
    # https://github.com/tox-dev/sphinx-autodoc-typehints
    'sphinx_autodoc_typehints'
]
templates_path = ['_templates']

# styling
html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']

# autosummary config
# https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html#generating-stub-pages-automatically
autosummary_generate = True

# autodoc config
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration
autoclass_content = "both"  # combine the __init__ doc into the class doc
# NOTE: don't use these options. They do not work very well
# autodoc_class_signature = 'separated'
# autodoc_typehints = 'description'

# sphinx_autodoc_typehints config
# https://github.com/tox-dev/sphinx-autodoc-typehints#options
# NOTE: don't turn this on, it duplicates method params
# always_document_param_types = True
typehints_defaults = 'comma'
