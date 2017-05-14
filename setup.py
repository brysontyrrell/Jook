#!/usr/bin/env python

from setuptools import setup
import re

with open('jook/__init__.py', 'r') as fobj:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fobj.read(), re.MULTILINE).group(1)

with open('README.rst', 'r') as fobj:
    long_description = fobj.read()

setup(
    name='jook',
    version=version,
    description='A Jamf Pro webhook simulator',
    long_description=long_description,
    url='https://github.com/brysontyrrell/Jook',
    author='Bryson Tyrrell',
    author_email='bryson.tyrrell@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='jamf webhooks testing',
    packages=['jook'],
    install_requires=[
        'dicttoxml>=1.7',
        'requests>=2.11'
    ],
    zip_safe=False
)
