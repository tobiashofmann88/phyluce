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

from phyluce.fetch import uce_counts
from phyluce.common import FullPaths, is_dir, is_file, CreateDir


descr = "Get the counts of UCE given a taxon list."


def configure_parser(sub_parsers):
    sp = sub_parsers.add_parser(
        "uce-counts",
        description=descr,
        help=descr
    )

    sp.add_argument(
        "--locus-db",
        required=True,
        action=FullPaths,
        type=is_file,
        help="The SQL database file holding probe matches to targeted loci "
             "(usually 'lastz/probe.matches.sqlite'.)"
    )
    sp.add_argument(
        "--taxon-list-config",
        required=True,
        action=FullPaths,
        type=is_file,
        help="The config file containing lists of the taxa you want to "
             "include in matrices."
    )
    sp.add_argument(
        "--taxon-group",
        required=True,
        type=str,
        help="The [group] in the config file whose specific data matrix "
             "you want to create.",
    )
    sp.add_argument(
        "--output",
        required=True,
        action=FullPaths,
        help="The path to the output file you want to create."
    )
    sp.add_argument(
        "--incomplete-matrix",
        action="store_true",
        default=False,
        help="Generate an incomplete matrix of data.",
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
    sp.add_argument(
        "--optimize",
        action="store_true",
        help="Return optimum groups of probes by enumeration (default) "
             "or sampling."
    )
    sp.add_argument(
        "--random",
        action="store_true",
        help="Optimize by sampling."
    )
    sp.add_argument(
        "--samples",
        type=int,
        default=10,
        help="The number of samples to take."
    )
    sp.add_argument(
        "--sample-size",
        dest="sample_size",
        type=int,
        default=10,
        help="The group size of samples."
    )
    sp.add_argument(
        "--extend-locus-db",
        action=FullPaths,
        type=is_file,
        help="An SQLlite database file holding probe matches to other "
             "targeted loci"
    )
    sp.add_argument(
        "--silent",
        dest="silent",
        action="store_true",
        help="Don\'t print probe names."
    )
    sp.add_argument(
        "--keep-counts",
        dest="keep_counts",
        action="store_true"
    )
    sp.set_defaults(func=get_uce_contig_counts)


def get_uce_contig_counts(args, parser):
    uce_counts.main(args, parser)
