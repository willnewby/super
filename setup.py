#!/usr/bin/env python

from setuptools import setup

VERSION = '0.0.3'
REQS = [
    'argparse',
    'boto',
    'salt'
    ]

setup(
    name = 'super',
    url = 'https://github.com/willnewby/super',
    description = 'A moderately complex devops tool utilizing salt-cloud and fabric',
    long_description = open('README.md').read(),
    version = VERSION,
    author = 'Will Newby',
    author_email = 'willnewby@gmail.com',
    license = 'GPL',
    install_requires = REQS,
    scripts = [ 'src/super' ],
    classifiers = [
        'Environment :: Console',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities',
    ]
)
