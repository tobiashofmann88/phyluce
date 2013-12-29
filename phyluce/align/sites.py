#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 28 December 2013 16:12 PST (-0800)
"""

from __future__ import absolute_import
import os
import multiprocessing
from Bio import AlignIO
from collections import Counter

from phyluce.log import setup_logging
from phyluce.common import get_alignment_files


def get_informative_sites(count):
    # remove gaps
    del count['-']
    # remove N
    del count['N']
    # remove ?
    del count['?']
    sufficient_sites = len(count)
    if sufficient_sites >= 2:
        sufficient_sequences = sum([1 for i in count.values() if i >= 2])
        if sufficient_sequences >= 2:
            return True
    return False


def get_differences(count):
    # remove gaps
    del count['-']
    # remove N
    del count['N']
    # remove ?
    del count['?']
    # remove X
    del count['X']
    sufficient_sites = len(count)
    # counted, different = (1,1)
    if sufficient_sites >= 2:
        return (1, 1)
    # counted, not different = (1,0)
    elif sufficient_sites == 1 and count.most_common()[0][1] > 1:
        return (1, 0)
    # not counted, not different = (0,0)
    else:
        return (0, 0)


def worker(work):
    args, f = work
    aln = AlignIO.read(f, args.input_format)
    name = os.path.basename(f)
    informative_sites = []
    differences = []
    counted_sites = []
    for idx in xrange(aln.get_alignment_length()):
        col = aln[:, idx].upper()
        count = Counter(col)
        if get_informative_sites(count):
            informative_sites.append(1)
        else:
            informative_sites.append(0)
        diff = get_differences(count)
        # sufficient in number and different
        if diff == (1, 1):
            counted_sites.append(1)
            differences.append(1)
        # sufficient in number, not different
        elif diff == (1, 0):
            counted_sites.append(1)
            differences.append(0)
        # removed from consideration
        else:
            differences.append(0)
            counted_sites.append(0)
    return (
        name,
        aln.get_alignment_length(),
        sum(informative_sites),
        sum(differences),
        sum(counted_sites)
    )


def main(args, parser):
    # setup logging
    log, my_name = setup_logging(args)
    files = get_alignment_files(
        log,
        args.alignments,
        args.input_format
    )
    work = [(args, f) for f in files]
    log.info("Computing informative sites using {} cores".format(args.cores))
    if args.cores > 1:
        assert args.cores <= multiprocessing.cpu_count(), ("You've specified "
                                                           "more cores than "
                                                           "you have")
        pool = multiprocessing.Pool(args.cores)
        results = pool.map(worker, work)
    else:
        results = map(worker, work)

    with open(args.output, 'w') as outf:
        outf.write(
            "locus,length,informative_sites,differences,counted-bases\n"
        )
        global_locus_length = []
        global_informative_sites = []
        global_differences = []
        global_counted_sites = []
        for locus in results:
            global_locus_length.append(locus[1])
            global_informative_sites.append(locus[2])
            global_differences.append(locus[3])
            global_counted_sites.append(locus[4])
            outf.write("{0},{1},{2},{3},{4}\n".format(
                locus[0],
                locus[1],
                locus[2],
                locus[3],
                locus[4]
            ))
        log.info("Total loci = {}".format(
            len(global_locus_length)
        ))
        log.info("Total BP considered = {}".format(
            sum(global_locus_length)
        ))
        log.info("Average BP per locus = {0:.2f}".format(
            sum(global_locus_length) / float(len(global_locus_length))
        ))
        log.info("Total informative sites = {0}".format(
            sum(global_informative_sites)
        ))
        log.info("Sites per locus = {0:.2f}".format(
            sum(global_informative_sites) / float(len(global_locus_length))
        ))
        log.info("Total differences = {0}".format(
            sum(global_differences)
        ))
        log.info("Differences per locus = {0:.2f}".format(
            sum(global_differences) / float(len(global_locus_length))
        ))
        log.info("All sites checked for differences = {0}".format(
            sum(global_counted_sites)
        ))
        log.info("Sites checked per locus = {0:.2f}".format(
            sum(global_counted_sites) / float(len(global_locus_length))
        ))
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
