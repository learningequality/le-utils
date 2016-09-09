import os
from distutils.command.install import INSTALL_SCHEMES
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setup(
    name = "fle-utils",
    version = "0.0.1",
    author = "Jordan Yoshihara",
    author_email = "jordan@learningequality.org",
    description = ("FLE utils and constants shared across kolibri, ricecooker and the content curation server."),
    license = "BSD",
    keywords = "fle le utils",
    url = "https://github.com/learningequality/fle-utils",
    # packages=['an_example_pypi_project', 'tests'],
    packages=find_packages(exclude=['tests']),
    # long_description=read('README'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
