#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 29 December 2013 12:28 PST (-0800)
"""

from __future__ import absolute_import
import os
import sys
import math
import shutil
import multiprocessing

from Bio import AlignIO

from phyluce.log import setup_logging
from phyluce.common import get_alignment_files

import pdb


def copy_over_files(work):
    sys.stdout.write('.')
    sys.stdout.flush()
    file, package = work
    args, min_count = package
    aln = AlignIO.read(file, args.input_format)
    if len(aln) >= min_count:
        new_file_pth = os.path.join(args.output, os.path.basename(file))
        shutil.copyfile(file, new_file_pth)
        return 1
    else:
        return 0


def compute_total_taxa(work):
    file, args = work
    aln = AlignIO.read(file, args.input_format)
    return len(aln)


def main(args, parser):
    # setup logging
    log, my_name = setup_logging(args)
    files = get_alignment_files(
        log,
        args.alignments,
        args.input_format
    )
    log.info("Counting taxa in {} alignments".format(len(files)))
    # get max number of taxa in all files
    work1 = [(file, args) for file in files]
    if args.cores > 1:
        assert args.cores <= multiprocessing.cpu_count(), ("You've specified "
                                                           "more cores than "
                                                           "you have")
        pool = multiprocessing.Pool(args.cores)
    else:
        pool = False
    if pool:
        counts = pool.map(compute_total_taxa, work1)
    else:
        counts = map(compute_total_taxa, work1)
    max_taxa = max(counts)
    if args.percent:
        # determine the minimum count of taxa needed in each alignment
        # given --percent
        min_count = int(math.floor((args.percent / 100.) * max_taxa))
        log.info("MAX(taxa) = {0}, keeping min_count = {1} ({2} * {0})".format(
            max_taxa,
            min_count,
            args.percent
        ))
    elif args.min_taxa:
        min_count = args.min_taxa
        log.info("MAX(taxa) = {}, keeping min_count = {}".format(
            max_taxa,
            min_count,
            args.percent
        ))
    log.info("Copying files of min_count {}".format(min_count))
    package = [args, min_count]
    work2 = [(file, package) for file in files]
    if pool:
        results = pool.map(copy_over_files, work2)
    else:
        results = map(copy_over_files, work2)
    print ""
    log.info("Copied {0} of {1} total alignments containing ≥ {2} "
             "min taxa (total taxa = {3})".format(sum(results),
                                                  len(results),
                                                  min_count,
                                                  max_taxa,
                                                  ))
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
