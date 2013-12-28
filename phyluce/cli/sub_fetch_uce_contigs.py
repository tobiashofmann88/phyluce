#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 27 December 2013 14:12 PST (-0800)
"""


from __future__ import absolute_import

from phyluce.fetch import uce_contigs
from phyluce.common import FullPaths, is_dir, is_file, CreateDir


descr = "Locate UCE contigs using LASTZ."


def configure_parser(sub_parsers):
    sp = sub_parsers.add_parser(
        "uce-contigs",
        description=descr,
        help=descr
    )
    sp.add_argument(
        '--contigs',
        required=True,
        type=is_dir,
        action=FullPaths,
        help="The directory containing the assembled contigs in which you "
             "are searching for UCE loci."
    )
    sp.add_argument(
        '--probes',
        required=True,
        type=is_file,
        action=FullPaths,
        help="The bait/probe file in FASTA format."
    )
    sp.add_argument(
        '--output',
        required=True,
        action=CreateDir,
        help="The directory in which to store the resulting SQL database"
             " and LASTZ files."
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
        '--min-coverage',
        default=80,
        type=int,
        help="The minimum percent coverage required for a match [default=80]."
    )
    sp.add_argument(
        '--min-identity',
        default=80,
        type=int,
        help="The minimum percent identity required for a match [default=80]."
    )
    sp.add_argument(
        '--dupefile',
        help="Path to self-to-self lastz results for baits to remove "
             "potential duplicate probes."
    )
    sp.add_argument(
        "--regex",
        type=str,
        default="^(uce-\d+)(?:_p\d+.*)",
        help="A regular expression to apply to the probe names for "
             "replacement [default='^(uce-\d+)(?:_p\d+.*)']."
    )
    sp.add_argument(
        "--keep-duplicates",
        type=str,
        default=None,
        help="A optional output file in which to store those loci that "
             "appear to be duplicates."
    )
    sp.set_defaults(func=get_uce_contigs)


def get_uce_contigs(args, parser):
    uce_contigs.main(args, parser)
