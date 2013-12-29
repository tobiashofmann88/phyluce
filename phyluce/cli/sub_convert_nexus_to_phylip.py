#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 29 December 2013 09:03 PST (-0800)
"""

from __future__ import absolute_import

from phyluce.convert import concat_nexus_to_phylip
from phyluce.common import is_dir, FullPaths, CreateDir


descr = "Concatenate NEXUS alignments to PHYLIP (RAXML) format."


def configure_parser(sub_parsers):
    sp = sub_parsers.add_parser(
        "concat-nexus-to-phylip",
        description=descr,
        help=descr
    )
    sp.add_argument(
        "--alignments",
        required=True,
        type=is_dir,
        action=FullPaths,
        help="The directory containing alignments to concatenate "
             "(NEXUS-ONLY)."
    )
    sp.add_argument(
        "--output",
        required=True,
        action=CreateDir,
        help="""The output file for the concatenated phylip data""",
    )
    sp.add_argument(
        "--charsets",
        action="store_true",
        default=False,
        help="""Add charsets to phylip file""",
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

    sp.set_defaults(func=nexus_to_phylip)


def nexus_to_phylip(args, parser):
    concat_nexus_to_phylip.main(args, parser)
