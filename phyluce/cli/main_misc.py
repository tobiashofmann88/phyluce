#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 29 December 2013 13:01 PST (-0800)
"""

from __future__ import absolute_import
import sys

from phyluce.cli import sub_misc_fasta


descr = "Miscellaneous utilities for files and directories."


def configure_parser(sub_parsers):
    if len(sys.argv) == 2:
        sys.argv.append("-h")
    p = sub_parsers.add_parser(
        "misc",
        description=descr,
        help=descr
    )

    sub_parsers = p.add_subparsers(
        metavar="command",
        dest="cmd",
    )

    sub_misc_fasta.configure_parser(sub_parsers)
