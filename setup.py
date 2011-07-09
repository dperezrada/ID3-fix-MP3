# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '0.0.2'

setup(
    name = 'id3fixmp3',
    version = version,
    keywords = 'id3fixmp3',
    description = '',
    author = 'Daniel Pérez Rada',
    packages = find_packages(exclude=['tests']),
    #Libraries needed for your project
    install_requires=[
      "ludibrio", "lxml", "httplib2"
    ]
)
