from setuptools import find_packages, setup

try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

requirements = [
    "pycountry==17.5.14",
]

setup(
    name="le-utils",
    packages = find_packages(),
    version="0.1.17",
    description="LE Utils and constants shared across Kolibri, Ricecooker, and the Kolibri Studio.",
    long_description=long_description,
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
