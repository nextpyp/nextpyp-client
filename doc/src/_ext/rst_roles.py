
from docutils.parsers.rst import roles
from docutils import nodes


# USAGE :strikethrough:`text`
def role_strikethrough(role, rawtext, text, lineno, inliner, options={}, content=[]):
    node = nodes.inline(rawtext, text, **{'classes': ['strike']})
    return [node], []


def setup(app):
    roles.register_canonical_role('strikethrough', role_strikethrough)
