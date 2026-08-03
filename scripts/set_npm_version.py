"""
set_npm_version
Writes the release version into js/package.json, for the npm publish path only.

Kept out of generate_from_specs.py on purpose. The version is derived from git
tags, so a tracked value can never match what setuptools-scm computes once a
release tag is created: the tag is applied to a commit whose package.json was
written before the tag existed. Regenerating it as part of `make build` made the
rebuild-from-specs hook fail on every commit after a release. The tracked value
is a 0.0.0 placeholder; only `make release-npm` sets a real one.
"""

import json
import os
import re
from importlib.metadata import version as get_version

package_json = os.path.join(os.path.dirname(__file__), "..", "js", "package.json")


def pep440_to_npm_semver(version):
    """Return version if it is an exact X.Y.Z release, else fail.

    setuptools-scm only returns a bare X.Y.Z for a checkout at a release tag.
    Anything else carries a dev/local suffix and would publish a version that
    does not correspond to a release.
    """
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        raise SystemExit("Refusing to set npm version from non-release version {!r}. Publish from a checkout at a release tag.".format(version))
    return version


def set_package_json_version():
    npm_version = pep440_to_npm_semver(get_version("le-utils"))

    with open(package_json, "r") as f:
        package = json.load(f)

    package["version"] = npm_version

    with open(package_json, "w") as f:
        output = json.dumps(package, indent=2, sort_keys=True)
        firstline = True
        for line in output.split("\n"):
            if firstline:
                firstline = False
            else:
                f.write("\n")
            f.write(line.rstrip())
        f.write("\n")
    return npm_version


if __name__ == "__main__":
    print("Set js/package.json version to {}".format(set_package_json_version()))
