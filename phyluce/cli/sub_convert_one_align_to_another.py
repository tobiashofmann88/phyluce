#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 29 December 2013 09:33 PST (-0800)
"""

from __future__ import absolute_import

from phyluce.convert import aligns_to_another
from phyluce.common import is_dir, FullPaths, CreateDir
from phyluce.align.var import align_io_choices


descr = "Convert a directory of alignments to another format."


def configure_parser(sub_parsers):
    sp = sub_parsers.add_parser(
        "one-format-to-another",
        description=descr,
        help=descr
    )
    sp.add_argument(
        "--alignments",
        required=True,
        type=is_dir,
        action=FullPaths,
        help="The directory containing alignments to convert"
    )
    sp.add_argument(
        '--output',
        required=True,
        action=CreateDir,
        help="The directory to hold the converted files",
    )
    sp.add_argument(
        "--input-format",
        dest="input_format",
        choices=align_io_choices,
        default="nexus",
        help="The input alignment format"
    )
    sp.add_argument(
        "--output-format",
        dest="output_format",
        choices=align_io_choices,
        default="fasta",
        help="The output alignment format"
    )
    sp.add_argument(
        "--cores",
        type=int,
        default=1,
        help="The number of compute cores to use"
    )
    group = sp.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--shorten-names",
        dest='shorten_name',
        action="store_true",
        default=False,
        help="Automatically convert names to a 6 or 7 character "
             "representation",
    )
    group.add_argument(
        "--name-conf",
        action=FullPaths,
        type=str,
        help="Use a CONFIG file to convert existing_names:new_names",
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

    sp.set_defaults(func=one_align_to_another)


def one_align_to_another(args, parser):
    aligns_to_another.main(args, parser)
