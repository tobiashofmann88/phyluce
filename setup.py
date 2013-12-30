#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

setup(
    name='phyluce',
    version='2.0.0',
    description='software for UCE (and general) phylogenomics',
    url='https://github.com/faircloth-lab/phyluce',
    author='Brant C. Faircloth',
    author_email='borg@faircloth-lab.org',
    license='BSD',
    platforms='any',
    packages=[
        'phyluce',
        'phyluce/align',
        'phyluce/assemble',
        'phyluce/cli',
        'phyluce/convert',
        'phyluce/fetch',
        'phyluce/misc'
    ],
    scripts=[
        'bin/phyluce'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    )
