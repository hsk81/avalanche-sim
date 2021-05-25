#!/usr/bin/env python
###############################################################################

from setuptools import setup

###############################################################################
###############################################################################

setup (
    name='avalanche-sim',
    version='1.3.0',
    description='Avalanche consensus simulator',
    author='Hasan Karahan',
    author_email='avalanche@blackhan.com',
    url='https://github.com/hsk81/avalanche-sim.git',
    install_requires=[
        'matplotlib>=3.4.1',
        'numpy>=1.20.2',
    ],
)

###############################################################################
###############################################################################
