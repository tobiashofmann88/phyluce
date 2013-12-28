#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 28 December 2013 12:12 PST (-0800)
"""

from __future__ import absolute_import
import os
import re
import ConfigParser
import multiprocessing

from Bio import AlignIO
from Bio.Alphabet import IUPAC, Gapped
from Bio.Align import MultipleSeqAlignment

from phyluce.common import get_alignment_files, record_formatter
from phyluce.align.common import copy_file
from phyluce.log import setup_logging


def repair_alignments(work):
    file, package = work
    format, regex, output = package
    # setup new align
    new_align = MultipleSeqAlignment([], Gapped(IUPAC.ambiguous_dna, "-?"))
    # read old align
    aln = AlignIO.read(file, format)
    for seq in aln:
        sequence = str(seq.seq)
        new_string = re.sub(regex, "N", sequence).upper()
        new_sequence = record_formatter(seq.name, new_string)
        new_align.append(new_sequence)
    with open(os.path.join(output, os.path.basename(file)), 'w') as outf:
        AlignIO.write(new_align, outf, 'nexus')
    return 1


def main(args, parser):
    # setup logging
    log, my_name = setup_logging(args)
    # find all alignments
    conf = ConfigParser.ConfigParser()
    conf.optionxform = str
    conf.read(args.config)
    bad_files = [item[0] for item in conf.items(args.section)]
    files = get_alignment_files(
        log,
        args.alignments,
        args.input_format
    )
    log.info("There are {} TOTAL files.".format(len(files)))
    log.info("There are {} BAD files.".format(len(bad_files)))
    expected_copy = len(files) - len(bad_files)
    # copy over files with no problems
    copied_names, bad_names = copy_file(
        files,
        bad_files,
        args.output,
        expected_copy
    )
    log.info("Copied {} files.".format(
        len(copied_names)
    ))
    package = (
        args.input_format,
        re.compile("[NXBDHKMSRWVYnxbdhkmsrwvy]"),
        args.output
    )
    work = [(f, package) for f in bad_names]
    log.info(
        "Screening alignments for problematic bases using {} cores".format(
            args.cores
        ))
    if args.cores > 1:
        assert args.cores <= multiprocessing.cpu_count(), ("You've specified "
                                                           "more cores than "
                                                           "you have")
        pool = multiprocessing.Pool(args.cores)
        repaired = pool.map(repair_alignments, work)
        pool.close()
    else:
        repaired = map(repair_alignments, work)
    log.info("Repaired (converted non-standard bases) {} files.".format(
        sum(repaired)
    ))
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
