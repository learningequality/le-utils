import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="le-utils",
    packages=["le_utils"],
    version="0.0.1",
    description="LE Utils and constants shared across Kolibri, Ricecooker and the Content Curation Server.",
    long_description=read('README.md'),
    license="MIT",
    url="https://github.com/learningequality/le-utils",
    downaload_url="https://github.com/learningequality/le-utils/tarball/0.0.1",
    keywords=["le-utils", "le_utils", "le utils", "kolibri", "ricecooker", "content curation"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
    author="Jordan Yoshihara",
    author_email="jordan@learningequality.org",
)
