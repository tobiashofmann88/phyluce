#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 29 December 2013 10:37 PST (-0800)
"""


from __future__ import absolute_import

from phyluce.align import extract
from phyluce.align.var import align_io_choices
from phyluce.common import is_dir, FullPaths, CreateDir


descr = "Extract taxa from a set of alignments."


def configure_parser(sub_parsers):
    sp = sub_parsers.add_parser(
        "extract",
        description=descr,
        help=descr,
    )

    sp.add_argument(
        "--alignments",
        required=True,
        action=FullPaths,
        type=is_dir,
        help="The directory containing alignments to extract taxa from."
    )
    sp.add_argument(
        "--output",
        required=True,
        action=CreateDir,
        help="The directory in which to store the resulting alignments."
    )
    group = sp.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--exclude',
        type=str,
        default=[],
        nargs='+',
        help='List of taxa to EXCLUDE'
    )
    group.add_argument(
        '--include',
        type=str,
        default=[],
        nargs='+',
        help='List of taxa to INCLUDE')
    # end mututally exclusive required group
    sp.add_argument(
        "--input-format",
        dest="input_format",
        choices=align_io_choices,
        default="nexus",
        help="The input alignment format"
    )
    sp.add_argument(
        "--output-format",
        dest="output_format",
        choices=align_io_choices,
        default="nexus",
        help="The output alignment format"
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
        help="""The logging level to use."""
    )
    sp.add_argument(
        "--log-path",
        action=FullPaths,
        type=is_dir,
        default=None,
        help="""The path to a directory to hold logs."""
    )

    sp.set_defaults(func=extract_taxa)


def extract_taxa(args, parser):
    extract.main(args, parser)
