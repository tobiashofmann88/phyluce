#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 28 December 2013 15:12 PST (-0800)
"""

from __future__ import absolute_import

from phyluce.align import sites
from phyluce.common import is_dir, FullPaths


descr = "Compute the number of informative sites."


def configure_parser(sub_parsers):
    sp = sub_parsers.add_parser(
        "sites",
        description=descr,
        help=descr,
    )

    sp.add_argument(
        '--alignments',
        required=True,
        action=FullPaths,
        type=is_dir,
        help="The directory containing the alignment files"
    )
    sp.add_argument(
        '--output',
        required=True,
        type=str,
        default=None,
        help="""The output filename"""
    )
    sp.add_argument(
        "--input-format",
        choices=["fasta", "nexus", "phylip", "clustal", "emboss", "stockholm"],
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
        help="""The logging level to use."""
    )
    sp.add_argument(
        "--log-path",
        action=FullPaths,
        type=is_dir,
        default=None,
        help="The path to a directory to hold logs."
    )

    sp.set_defaults(func=compute_sites)


def compute_sites(args, parser):
    sites.main(args, parser)
