#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 27 December 2013 16:12 PST (-0800)
"""


from __future__ import absolute_import

from phyluce.align import stats
from phyluce.common import is_dir, FullPaths


descr = "Compute alignment stats."


def configure_parser(sub_parsers):
    sp = sub_parsers.add_parser(
        "stats",
        description=descr,
        help=descr
    )

    sp.add_argument(
        "--alignments",
        required=True,
        type=is_dir,
        action=FullPaths,
        help="The directory containing alignments to be summarized."
    )
    sp.add_argument(
        "--input-format",
        dest="input_format",
        choices=[
            "fasta",
            "nexus",
            "phylip",
            "phylip-relaxed",
            "clustal",
            "emboss",
            "stockholm"
        ],
        default="nexus",
        help="The input alignment format.",
    )
    sp.add_argument(
        "--show-taxon-counts",
        action="store_true",
        default=False,
        help="Show the count of loci with X taxa.",
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
    sp.add_argument(
        "--cores",
        type=int,
        default=1,
        help="Process alignments in parallel using --cores for alignment. "
             "This is the number of PHYSICAL CPUs."
    )

    sp.set_defaults(func=get_alignment_stats)


def get_alignment_stats(args, parser):
    stats.main(args, parser)
