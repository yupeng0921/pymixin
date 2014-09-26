try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

mixin_classifiers = [
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
]

import mixin

with open("README.md", "r") as f:
    mixin_long_description = f.read()

setup(
    name = "mixin",
    version = mixin.__version__,
    keywords = ("mixin"),
    description = "python mixin tool",
    long_description=mixin_long_description,
    license = "MIT",
    url = "https://github.com/yupeng820921/pymixin",
    author = "yupeng",
    author_email = "yupeng0921@gmail.com",
    platforms = 'any',
    classifiers=mixin_classifiers,
)
