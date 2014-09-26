from setuptools import setup, find_packages

mixin_classifiers = [
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
]

import mixin

setup(
    name = "mixin",
    version = mixin.__version__,
    keywords = ("mixin"),
    description = "python mixin tool",
    license = "MIT",
    url = "https://github.com/yupeng820921/pymixin",
    author = "yupeng",
    author_email = "yupeng0921@gmail.com",
    platforms = 'any',
    classifiers=mixin_classifiers,
)
