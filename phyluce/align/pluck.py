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
import sys
import multiprocessing

from Bio import AlignIO

from phyluce.log import setup_logging
from phyluce.common import get_alignment_files, record_formatter


def extract_taxon(work):
    sys.stdout.write('.')
    sys.stdout.flush()
    file, args = work
    locus = os.path.splitext(os.path.basename(file))[0]
    aln = AlignIO.read(file, args.input_format)
    #pdb.set_trace()
    for seq in aln:
        if seq.id == args.taxon:
            # replace insertions and missing data designators
            seq_string = re.sub("[\?-]*", "", str(seq.seq))
            if not len(seq_string) == 0:
                new_seq = record_formatter(locus, seq_string)
            else:
                new_seq = None
            break
        else:
            new_seq = None

    return locus, new_seq


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
    work = [(file, args) for file in files]
    log.info("Plucking alignments using {} cores".format(args.cores))
    if args.cores > 1:
        assert args.cores <= multiprocessing.cpu_count(), ("You've specified "
                                                           "more cores than "
                                                           "you have")
        pool = multiprocessing.Pool(args.cores)
        sequences = pool.map(extract_taxon, work)
    else:
        sequences = map(extract_taxon, work)
    print ""
    with open(args.output, 'w') as outf:
        for locus, seq in sequences:
            if seq is not None:
                outf.write(seq.format("fasta"))
            else:
                log.info("Locus {} dropped because sequence length was"
                         " 0 or taxon was not present".format(locus))
    # done
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
