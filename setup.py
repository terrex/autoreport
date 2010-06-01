# -*- coding: utf-8 -*-

import os

from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='autoreport',
    version='0.1',
    description='Self-made relatorio reports for Django',
    author=u'Guillermo Gutiérrez',
    author_email='xiterrex@gmail.com',
    url='http://github.com/terrex/autoreport',
    include_package_data=True,
    packages=['autoreport'],
    long_description=read('README'),
    license='GPL',
    install_requires=[
        'Django>=1.1.1',
        'relatorio>=0.5'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: XML'
    ]
)
