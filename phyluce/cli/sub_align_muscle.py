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

from phyluce.align import common, common_args


descr = "Align UCE FASTA data using MUSCLE."


def configure_parser(sub_parsers, engine):
    sp = sub_parsers.add_parser(
        'muscle',
        description=descr,
        help=descr
    )
    sp = common_args.shared(sp)
    sp.set_defaults(func=align_with_muscle)


def align_with_muscle(args, parser):
    from phyluce.align.engines import Muscle
    common.main(args, parser, Muscle)
