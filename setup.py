from setuptools import find_packages, setup

with open('README.md') as file:
    long_description = file.read()


requirements = [
    "pycountry==17.5.14",
]

setup(
    name="le-utils",
    packages = find_packages(),
    version="0.0.12",
    description="LE Utils and constants shared across Kolibri, Ricecooker and the Content Curation Server.",
    long_description=long_description,
    install_requires=requirements,
    license="MIT",
    url="https://github.com/learningequality/le-utils",
    download_url="https://github.com/learningequality/le-utils/tarball/0.0.9c14",
    keywords="le-utils le_utils le utils kolibri ricecooker content curation",
    package_data={"le_utils": ["resources/*.json"], },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
    author="Jordan Yoshihara",
    author_email="jordan@learningequality.org", )
