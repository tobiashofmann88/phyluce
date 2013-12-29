#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 29 December 2013 09:09 PST (-0800)
"""

from __future__ import absolute_import
import os
import glob
from Bio.Nexus import Nexus

from phyluce.log import setup_logging


def main(args, parser):
    # setup logging
    log, my_name = setup_logging(args)
    # read alignments
    log.info("Reading input alignments in NEXUS format")
    nexus_files = glob.glob(os.path.join(args.alignments, '*.nex*'))
    data = [(os.path.basename(fname), Nexus.Nexus(fname))
            for fname in nexus_files]
    log.info("Concatenating {} NEXUS files to PHYLIP (RAXML) format".format(
        len(nexus_files)
    ))
    concatenated = Nexus.combine(data)
    concat_file = os.path.join(
        args.output,
        os.path.basename(args.alignments) + ".phylip"
    )
    if args.charsets:
        sets = concatenated.append_sets()
        charset_file = os.path.join(
            args.output,
            os.path.basename(args.alignments) + ".charsets"
        )
        log.info("Writing charsets to {}".format(charset_file))
        with open(charset_file, 'w') as outf:
            outf.write(sets)
    log.info("Writing concatenated PHYLIP alignment to {}".format(
        concat_file
    ))
    concatenated.export_phylip(concat_file)
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
