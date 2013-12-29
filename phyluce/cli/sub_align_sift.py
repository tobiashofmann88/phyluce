#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 29 December 2013 12:21 PST (-0800)
"""


from __future__ import absolute_import

from phyluce.align import sift
from phyluce.align.var import align_io_choices
from phyluce.common import is_dir, FullPaths, CreateDir


descr = ("Sift alignments and output those with more than --percent-taxa or "
         "more than --min-taxa.")


def configure_parser(sub_parsers):
    sp = sub_parsers.add_parser(
        "sift",
        description=descr,
        help=descr,
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
        required=True,
        action=CreateDir,
        help="The directory in which to store the resulting alignments."
    )
    group = sp.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--min-taxa",
        type=int,
        default=None,
        help="The minimum number of taxa in all alignments."
    )
    group.add_argument(
        "--percent",
        type=float,
        choices=range(0, 100),
        default=None,
        help="The minimum percent of taxa in all alignments"
    )
    sp.add_argument(
        "--input-format",
        choices=align_io_choices,
        default="nexus",
        help="The input alignment format.",
    )
    sp.add_argument(
        "--cores",
        type=int,
        default=1,
        help="Process alignments in parallel using --cores for alignment. "
             "This is the number of PHYSICAL CPUs."
    )
    sp.add_argument(
        "--verbosity",
        type=str,
        choices=["INFO", "WARN", "CRITICAL"],
        default="INFO",
        help="The logging level to use."
    )
    sp.add_argument(
        "--log-path",
        action=FullPaths,
        type=is_dir,
        default=None,
        help="The path to a directory to hold logs."
    )

    sp.set_defaults(func=sift_alignments)


def sift_alignments(args, parser):
    sift.main(args, parser)
