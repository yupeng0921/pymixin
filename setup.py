from setuptools import setup, find_packages

PACKAGE = "mixin"
NAME = "mixin"
KEYWORDS = ("mixin")
VERSION = '0.1'
DESCRIPTION = "pythone mixin tool"
LICENSE = 'MIT License'
URL = ""
AUTHOR = "yupeng"
AUTHOR_EMAIL = "yupeng0921@gmail.com"

setup(
        name = NAME,
        version = VERSION,
        keywords = KEYWORDS,
        description = DESCRIPTION,
        license = LICENSE,

        url = URL,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,

        packages = find_packages(),
        include_package_data = True,
        platforms = 'any',
        install_requires = [],
)
