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

from phyluce.align import clean
from phyluce.common import is_dir, FullPaths, CreateDir


descr = "Clean a set of newly-aligned UCE data."


def configure_parser(sub_parsers):
    sp = sub_parsers.add_parser(
        "clean",
        description=descr,
        help=descr,
    )

    sp.add_argument(
        "--alignments",
        required=True,
        action=FullPaths,
        type=is_dir,
        help="The input directory containing alignment (nexus) files to "
             "filter"
    )
    sp.add_argument(
        "--output",
        required=True,
        action=CreateDir,
        help="The output directory to hold the cleaned nexus files",
    )
    sp.add_argument(
        "--taxa",
        type=int,
        default=None,
        help="""The expected number of taxa in all alignments""",
    )
    sp.add_argument(
        "--input-format",
        choices=["fasta", "nexus", "phylip", "clustal", "emboss", "stockholm"],
        default="nexus",
        help="The input alignment format.",
    )
    sp.add_argument(
        "--output-format",
        choices=["fasta", "nexus", "phylip", "clustal", "emboss", "stockholm"],
        default="nexus",
        help="The output alignment format.",
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
    sp.set_defaults(func=clean_alignments)


def clean_alignments(args, parser):
    clean.main(args, parser)
