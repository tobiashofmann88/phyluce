#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 28 December 2013 13:12 PST (-0800)
"""


from __future__ import absolute_import

from phyluce.align import explode
from phyluce.common import is_dir, is_file, FullPaths, CreateDir


descr = ("Explode a set of alignment files by-locus or by-taxon into "
         "the consituent set of FASTA sequence files.")


def configure_parser(sub_parsers):
    sp = sub_parsers.add_parser(
        "explode",
        description=descr,
        help=descr,
    )

    sp.add_argument(
        "--alignments",
        required=True,
        action=FullPaths,
        type=is_dir,
        help="The directory containing alignments to be blown up."
    )
    sp.add_argument(
        "--output",
        required=True,
        action=CreateDir,
        help="The directory in which to store the resulting FASTA files."
    )
    sp.add_argument(
        "--by-taxon",
        action="store_true",
        default=False,
        help="""Explode alignments by taxon instead of by-locus""",
    )
    sp.add_argument(
        "--input-format",
        dest="input_format",
        choices=['fasta', 'nexus', 'phylip', 'clustal', 'emboss', 'stockholm'],
        default='nexus',
        help="The input alignment format"
    )
    sp.add_argument(
        "--conf",
        action=FullPaths,
        type=is_file,
        help="Config file for renaming",
    )
    sp.add_argument(
        "--section",
        type=str,
        help="Section of config file to use",
    )
    sp.add_argument(
        "--exclude",
        type=str,
        nargs='+',
        default=[],
        help="Taxa/taxon to exclude",
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

    sp.set_defaults(func=explode_alignments)


def explode_alignments(args, parser):
    explode.main(args, parser)

