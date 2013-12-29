#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 29 December 2013 09:19 PST (-0800)
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
    log.info("Concatenating {} NEXUS files to NEXUS (garli) format".format(
        len(nexus_files)
    ))
    concatenated = Nexus.combine(data)
    concat_file = os.path.join(
        args.output,
        os.path.basename(args.alignments) + ".nexus"
    )
    if args.charsets:
        log.info("Writing concatenated alignment to NEXUS format "
                 "(with charsets)")
        concatenated.write_nexus_data(concat_file)
    else:
        log.info("Writing concatenated alignment to NEXUS format "
                 "(without charsets)")
        concatenated.write_nexus_data(concat_file, append_sets=False)
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
