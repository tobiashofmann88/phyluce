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

from phyluce.assembly import velvet
from phyluce.common import FullPaths, is_dir, is_file, CreateDir


descr = "Assemble reads using velvet."


def configure_parser(sub_parsers):
    sp = sub_parsers.add_parser(
        'velvet',
        description=descr,
        help=descr
    )
    # one of these is required.  The other will be set to None.
    input = sp.add_mutually_exclusive_group(required=True)
    input.add_argument(
        "--config",
        type=is_file,
        action=FullPaths,
        default=None,
        help="A configuration file containing reads to assemble"
    )
    input.add_argument(
        "--dir",
        type=is_dir,
        action=FullPaths,
        default=None,
        help="A directory of reads to assemble",
    )
    sp.add_argument(
        "--output",
        required=True,
        action=CreateDir,
        default=None,
        help="The directory in which to store the assembly data"
    )
    sp.add_argument(
        "--kmer",
        type=int,
        default=31,
        help="The kmer value to use"
    )
    sp.add_argument(
        "--cores",
        type=int,
        default=1,
        help="The number of compute cores/threads to run with Velvet"
    )
    sp.add_argument(
        "--subfolder",
        type=str,
        default='',
        help="A subdirectory, below the level of the group, containing "
             "the reads"
    )
    sp.add_argument(
        "--verbosity",
        type=str,
        choices=["INFO", "WARN", "CRITICAL"],
        default="INFO",
        help="The logging level to use"
    )
    sp.add_argument(
        "--log-path",
        action=FullPaths,
        type=is_dir,
        default=None,
        help="The path to a directory to hold logs."
    )
    sp.add_argument(
        "--clean",
        action="store_true",
        default=False,
        help="Cleanup all intermediate Trinity files",
    )
    sp.set_defaults(func=run_velvet_assembly)


def run_velvet_assembly(args, parser):
    velvet.main(args, parser)
