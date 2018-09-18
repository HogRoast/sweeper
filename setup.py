# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "Footy"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = []

setup(
    name=NAME,
    version=VERSION,
    description="Footy prediction algo",
    author_email="",
    url="",
    keywords=["Footy prediction algo"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={},
    include_package_data=True,
    entry_points={},
    long_description=""
)

