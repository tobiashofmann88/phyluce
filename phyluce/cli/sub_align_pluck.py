#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 29 December 2013 11:17 PST (-0800)
"""

from __future__ import absolute_import

from phyluce.align import pluck
from phyluce.align.var import align_io_choices
from phyluce.common import is_dir, FullPaths


descr = ("Pluck taxon from a set of alignments. Output plucked "
         "taxon as FASTA sequence file.")


def configure_parser(sub_parsers):
    sp = sub_parsers.add_parser(
        "pluck",
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
        type=str,
        help="The file in which to store the FASTA data."
    )
    sp.add_argument(
        "--taxon",
        required=True,
        type=str,
        help="""The taxon to extract"""
    )
    sp.add_argument(
        "--input-format",
        dest="input_format",
        choices=align_io_choices,
        default="nexus",
        help="The input alignment format"
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

    sp.set_defaults(func=pluck_taxa)


def pluck_taxa(args, parser):
    pluck.main(args, parser)
