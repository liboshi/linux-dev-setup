#1/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import codecs
import os
import re
import sys

from setuptools import find_packages
from setuptools import setup

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

install_requires = [
    'six >= 1.3.0, < 2',
]

setup(
    name = 'linux-dev-setup',
    version = find_version('__init__.py'),
    description = 'Linux development environment setup',
    url = 'https://github.com/liboshi/linux-dev-setup',
    author = 'Boush Li',
    license = 'MIT',
    packages = find_packages(exclude = ['test.*']),
    include_package_data = False,
    install_requires = install_requires,
    extras_require = extras_require,
    tests_require = tests_require,
)