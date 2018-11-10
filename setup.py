# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "sweeper"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ['sphinx>=1.8.1']

setup(
    name=NAME,
    version=VERSION,
    description="Sweeper - football prediction algo",
    author_email="monkeeferret@gmail.com",
    url="https://github.com/HogRoast/sweeper/",
    keywords=["Sweeper football prediction algo"],
    install_requires=REQUIRES,
    python_requires=">=3.7",
    packages=find_packages(),
    package_data={
        # If any package contains txt, sql, db or tmpl files, include them:
        '': ['*.txt', '*.sql', '*.db'],
    },
    include_package_data=True,
    entry_points={},
    long_description=""
)

