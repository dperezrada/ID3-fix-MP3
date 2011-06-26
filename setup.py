# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

setup(name='id3fixmp3',
    version=version,
    keywords='id3fixmp3',
    author='Daniel Pérez Rada',
    packages=find_packages(exclude=['tests']),
    install_requires=[
      "mutagen", "httplib2", "ludibrio", "lxml"
    ]
)
