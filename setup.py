import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="fle-utils",
    packages=["fle-utils"],
    version="0.0.1",
    description="FLE Utils and constants shared across Kolibri, Ricecooker and the Content Curation Server.",
    long_description=read('README'),
    license="MIT",
    url="https://github.com/learningequality/fle-utils",
    downaload_url="https://github.com/learningequality/fle-utils/tarball/0.0.1",
    keywords=["fle-utils", "fle_utils", "fle", "kolibri", "ricecooker", "content curation"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
    author="Jordan Yoshihara",
    author_email="jordan@learningequality.org",
)
