#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 27 December 2013 15:12 PST (-0800)
"""


from __future__ import absolute_import

from phyluce.align import common_args
from phyluce.common import FullPaths, is_dir, is_file, CreateDir


descr = "Align UCE FASTA data using MAFFT."


def configure_parser(sub_parsers, engine):
    sp = sub_parsers.add_parser(
        'mafft',
        description=descr,
        help=descr
    )
    sp = common_args.shared(sp)
    #pdb.set_trace()
    sp.set_defaults(func=align_with_mafft)


def align_with_mafft(args, parser):
    from phyluce.align.engines import Mafft
    common.main(args, parser, mafft)
