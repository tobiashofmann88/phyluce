#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 29 December 2013 10:40 PST (-0800)
"""

from __future__ import absolute_import
import os
import re

from Bio import AlignIO

from phyluce.log import setup_logging
from phyluce.common import get_alignment_files, record_formatter


def main(args, parser):
    # setup logging
    log, my_name = setup_logging(args)
    files = get_alignment_files(
        log,
        args.alignments,
        args.input_format
    )
    log.info("Plucking {} from {} {} alignments".format(
        args.taxon,
        len(files),
        args.input_format
    ))
    with open(args.output, 'w') as outf:
        for file in files:
            aln = AlignIO.read(file, args.input_format)
            for taxon in aln:
                if taxon.id == args.taxon:
                    # replace insertions and missing data designators
                    seq_string = re.sub("[\?-]*", "", str(taxon.seq))
                    locus = os.path.splitext(os.path.basename(file))[0]
                    if not len(seq_string) == 0:
                        new_seq = record_formatter(locus, seq_string)
                        outf.write(new_seq.format("fasta"))
                    else:
                        print locus
    # done
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
