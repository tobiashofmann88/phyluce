#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 27 December 2013 13:12 PST (-0800)
"""

from __future__ import absolute_import

from phyluce.cli import sub_assemble_velvet
from phyluce.cli import sub_assemble_abyss


descr = "Methods to assemble cleaned sequencing reads."

def configure_parser(sub_parsers):
    p = sub_parsers.add_parser('assemble', description=descr, help=descr)

    sub_parsers = p.add_subparsers(
        metavar = "command",
        dest = "cmd",
    )

    sub_assemble_velvet.configure_parser(sub_parsers)
    sub_assemble_abyss.configure_parser(sub_parsers)
