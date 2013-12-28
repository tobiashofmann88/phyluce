#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 28 December 2013 10:12 PST (-0800)
"""

from __future__ import absolute_import

from phyluce.align import check
from phyluce.common import is_dir, FullPaths


descr = "Check alignments for problems."


def configure_parser(sub_parsers):
    sp = sub_parsers.add_parser(
        "check",
        description=descr,
        help=descr
    )

    sp.add_argument(
        '--alignments',
        required=True,
        type=is_dir,
        action=FullPaths,
        help="The directory containing alignments to be screened."
    )
    sp.add_argument(
        '--output',
        action=FullPaths,
        help="The path to an output (conf) file to hold results."
    )
    sp.add_argument(
        '--do-not-screen-n',
        action="store_true",
        default=False,
        help="Do not screen alignments for taxa containing ambiguous (N)"
             "bases."
    )
    sp.add_argument(
        '--do-not-screen-x',
        action="store_true",
        default=False,
        help="Do not screen alignments for taxa containing ambiguous (X) "
             "bases."
    )
    sp.add_argument(
        '--do-not-screen-iupac',
        action="store_true",
        default=False,
        help="Do not screen alignments for taxa containing IUPAC "
             "(BDHKMSRWVY) bases."
    )
    sp.add_argument(
        "--input-format",
        dest="input_format",
        choices=['fasta', 'nexus', 'phylip', 'clustal', 'emboss', 'stockholm'],
        default='nexus',
        help="The input alignment format",
    )
    sp.add_argument(
        "--cores",
        type=int,
        default=1,
        help="Process alignments in parallel using --cores for alignment. "
             "This is the number of PHYSICAL CPUs."
    )
    sp.add_argument(
        "--log-path",
        action=FullPaths,
        type=is_dir,
        default=None,
        help="The path to a directory to hold logs."
    )
    sp.add_argument(
        "--verbosity",
        type=str,
        choices=["INFO", "WARN", "CRITICAL"],
        default="INFO",
        help="The logging level to use."
    )

    sp.set_defaults(func=check_alignments)


def check_alignments(args, parser):
    check.main(args, parser)
