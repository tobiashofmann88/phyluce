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

from phyluce.common import FullPaths, is_dir, is_file, CreateDir


def shared(sp):
    sp.add_argument(
        "--fasta",
        required=True,
        action=FullPaths,
        type=is_file,
        help="""The file containing FASTA reads associated with targted loci from """ +
        """get_fastas_from_match_counts.py"""
    )
    sp.add_argument(
        "--output",
        required=True,
        action=CreateDir,
        help="""The directory in which to store the resulting alignments."""
    )
    sp.add_argument(
        "--taxa",
        required=True,
        type=int,
        help="""Number of taxa expected in each alignment."""
    )
    sp.add_argument(
        "--output-format",
        choices=["fasta", "nexus", "phylip", "clustal", "emboss", "stockholm"],
        default="nexus",
        help="""The output alignment format.""",
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
        "--incomplete-matrix",
        dest="notstrict",
        action="store_true",
        default=False,
        help="""Allow alignments that do not contain all --taxa."""
    )
    sp.add_argument(
        "--no-trim",
        action="store_true",
        default=False,
        help="""Align, but DO NOT trim alignments."""
    )
    sp.add_argument(
        "--window",
        type=int,
        default=20,
        help="""Sliding window size for trimming."""
    )
    sp.add_argument(
        "--proportion",
        type=float,
        default=0.65,
        help="""The proportion of taxa required to have sequence at alignment ends."""
    )
    sp.add_argument(
        "--threshold",
        type=float,
        default=0.65,
        help="""The proportion of residues required across the window in """ +
        """proportion of taxa."""
    )
    sp.add_argument(
        "--max-divergence",
        type=float,
        default=0.20,
        help="""The max proportion of sequence divergence allowed between any row """ +
        """of the alignment and the alignment consensus."""
    )
    sp.add_argument(
        "--min-length",
        type=int,
        default=100,
        help="""The minimum length of alignments to keep."""
    )
    sp.add_argument(
        "--ambiguous",
        action="store_true",
        default=False,
        help="""Allow reads in alignments containing N-bases."""
    )
    sp.add_argument(
        "--cores",
        type=int,
        default=1,
        help="""Process alignments in parallel using --cores for alignment. """ +
        """This is the number of PHYSICAL CPUs."""
    )
    return sp
