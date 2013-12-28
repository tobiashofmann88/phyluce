#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 28 December 2013 10:12 PST (-0800)
"""

from __future__ import absolute_import
import os
import re
import ConfigParser
import multiprocessing
from collections import Counter
from Bio import AlignIO

from phyluce.common import get_alignment_files
from phyluce.log import setup_logging


def find_bad_bases(file_name, regex_names, regex, aln):
    result = None
    count = Counter()
    for seq in aln:
        findall_list = regex.findall(str(seq.seq))
        if findall_list:
            for result in findall_list:
                for pos, val in enumerate(result):
                    if val is not '':
                        count[regex_names[pos]] += 1
    if count.items() == []:
        count = None
    return (file_name, count)


def screen_files(work):
    format, file, regex_names, regex = work
    aln = AlignIO.read(file, format)
    file_name = os.path.basename(file)
    results = find_bad_bases(file_name, regex_names, regex, aln)
    return results


def build_total_regex(args):
    names = []
    regex = []
    if not args.do_not_screen_n:
        names.append("n")
        regex.append("(N|n)+")
    if not args.do_not_screen_x:
        names.append("x")
        regex.append("(X|x)+")
    if not args.do_not_screen_iupac:
        names.append("i")
        regex.append("([BDHKMSRWVYbdhkmsrwvy])+")
    assert len(regex) >= 1, ("You must specify at least one type of error to "
                             "check for.")
    return names, re.compile("|".join(regex))


def main(args, parser):
    # setup logging
    log, my_name = setup_logging(args)
    # find all alignments
    files = get_alignment_files(
        log,
        args.alignments,
        args.input_format
    )
    names, regex = build_total_regex(args)
    work = [(args.input_format, file, names, regex) for file in files]
    log.info(
        "Screening alignments for problematic bases using {} cores".format(
            args.cores
        )
    )
    if args.cores > 1:
        assert args.cores <= multiprocessing.cpu_count(), ("You've specified "
                                                           "more cores than "
                                                           "you have")
        pool = multiprocessing.Pool(args.cores)
        results = pool.map(screen_files, work)
        pool.close()
    else:
        results = map(screen_files, work)
    good = 0
    bad = 0
    config = ConfigParser.ConfigParser()
    config.add_section('Problematic loci')
    for result in results:
        name, counter = result
        if counter is not None:
            config.set('Problematic loci', name, dict(counter))
            log.info("Locus {} is problematic: {}".format(
                name,
                dict(counter)
            ))
            bad += 1
        else:
            good += 1
    if args.output:
        with open(args.output, 'wb') as outf:
            config.write(outf)
    log.info("There were {} GOOD alignments".format(good))
    log.info("There were {} BAD alignments".format(bad))
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
