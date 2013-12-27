#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 26 December 2013 16:12 PST (-0800)
"""


from __future__ import absolute_import
from phyluce.core import helpers


descr = "Match UCE probes/baits to assembled contigs."

'''
help =  (descr.replace(".", " ") +
        "and store the data in a relational database.  The matching process is dependent on the " +
        "probe names in the file.  If the probe names are not like 'uce-1001_p1' where 'uce-' " +
        "indicates we're searching for uce loci, '1001' indicates locus 1001, '_p1' indicates " +
        "this is probe 1 for locus 1001, you will need to set the optional --regex parameter. " +
        "So, if your probe names are 'MyProbe-A_probe1', the --regex will look like " +
        "--regex='^(MyProbe-\W+)(?:_probe\d+.*)'")
'''

def configure_parser(sub_parsers):
    p = sub_parsers.add_parser(
        'match',
        description=descr,
        help=descr
    )
    p.add_argument(
        '--contigs',
        required=True,
        #type=helpers.is_dir,
        action=helpers.FullPaths,
        help="The directory containing the assembled contigs in which you are searching for UCE loci."
    )
    p.add_argument(
        '--probes',
        required=True,
        #type=helpers.is_file,
        action=helpers.FullPaths,
        help="The bait/probe file in FASTA format."
    )
    p.add_argument(
        '--output',
        required=True,
        action=helpers.FullPaths,
        help="The directory in which to store the resulting SQL database and LASTZ files."
    )
    p.add_argument(
        "--verbosity",
        type=str,
        choices=["INFO", "WARN", "CRITICAL"],
        default="INFO",
        help="""The logging level to use."""
    )
    p.add_argument(
        "--log-path",
        action=helpers.FullPaths,
        #type=helpers.is_dir,
        default=None,
        help="""The path to a directory to hold logs."""
    )
    p.add_argument(
        '--min-coverage',
        default=80,
        type=int,
        help="The minimum percent coverage required for a match [default=80]."
    )
    p.add_argument(
        '--min-identity',
        default=80,
        type=int,
        help="The minimum percent identity required for a match [default=80]."
    )
    p.add_argument(
        '--dupefile',
        help="Path to self-to-self lastz results for baits to remove potential duplicate probes."
    )
    p.add_argument(
        "--regex",
        type=str,
        default="^(uce-\d+)(?:_p\d+.*)",
        help="""A regular expression to apply to the probe names for replacement [default='^(uce-\d+)(?:_p\d+.*)'].""",
    )
    p.add_argument(
        "--keep-duplicates",
        type=str,
        default=None,
        help="""A optional output file in which to store those loci that appear to be duplicates.""",
    )
    p.set_defaults(func=execute)


def execute(args, parser):
    from phyluce import match
    match.main(args, parser)
