from pathlib import Path

import semver
import toml

from nextpyp.client.gen import API_VERSION


PYPROJECT = Path(__file__).resolve().parents[3] / 'pyproject.toml'


def test_package_version_matches_api_version():
    """
    The package version tracks the nextPYP API version that gen.py was generated for:
    client X.Y.* speaks API X.Y. Regenerating gen.py for a new API without bumping
    the version in pyproject.toml (or the other way around) fails here.
    """
    package = semver.Version.parse(toml.load(PYPROJECT)['project']['version'])
    api = semver.Version.parse(API_VERSION)
    assert (package.major, package.minor) == (api.major, api.minor), \
        f'pyproject.toml version {package} doesn\'t match gen.py API_VERSION {api}'
