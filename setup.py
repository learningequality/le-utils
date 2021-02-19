import io
from setuptools import find_packages, setup

long_description = io.open('README.md', encoding='utf-8').read()

requirements = [
    "pycountry==17.5.14",
]

setup(
    name="le-utils",
    packages = find_packages(),
    version="0.1.27",
    description="LE-Utils contains shared constants used in Kolibri, Ricecooker, and Kolibri Studio.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    license="MIT",
    url="https://github.com/learningequality/le-utils",
    download_url="https://github.com/learningequality/le-utils/releases",
    keywords="le-utils le_utils LE utils kolibri studio ricecooker content curation",
    package_data={"le_utils": ["resources/*.json"],},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
    author="Jordan Yoshihara",
    author_email="jordan@learningequality.org",
)
