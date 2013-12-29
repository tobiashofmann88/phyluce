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
import sys
import multiprocessing

from Bio import AlignIO
from Bio.Alphabet import IUPAC, Gapped
from Bio.Align import MultipleSeqAlignment as Alignment

from phyluce.log import setup_logging
from phyluce.common import get_alignment_files


def get_taxa_to_keep(args, all_names):
    """docstring for get_samples_to_run"""
    if args.exclude:
        return set([name for name in all_names if name not in args.exclude])
    elif args.include:
        return set([name for name in all_names if name in args.include])
    else:
        return all_names


def get_all_taxon_names(format, files):
    taxa = set()
    for align_file in files:
        for align in AlignIO.parse(align_file, format):
            for taxon in list(align):
                #pdb.set_trace()
                taxa.add(taxon.name)
    return taxa


def remove_taxon_from_alignments(work):
    sys.stdout.write('.')
    sys.stdout.flush()
    file, args, taxa_to_keep = work
    new_align = Alignment([], alphabet=Gapped(IUPAC.unambiguous_dna, "-?"))
    aln = AlignIO.read(file, args.input_format)
    for seq in aln:
        if seq.id in taxa_to_keep:
            new_align.append(seq)
        else:
            pass
    outf_name = os.path.join(
        args.output,
        os.path.basename(file)
    )
    if len(new_align) > 1:
        with open(outf_name, 'w') as outf:
            AlignIO.write(new_align, outf, args.output_format)
        return None
    else:
        return os.path.basename(file)


def main(args, parser):
    # setup logging
    log, my_name = setup_logging(args)
    files = get_alignment_files(
        log,
        args.alignments,
        args.input_format
    )
    taxa = get_all_taxon_names(args.input_format, files)
    taxa_to_keep = get_taxa_to_keep(args, taxa)
    work = [(file, args, taxa_to_keep) for file in files]
    log.info("Extracting alignments using {} cores".format(args.cores))
    if args.cores > 1:
        assert args.cores <= multiprocessing.cpu_count(), ("You've specified "
                                                           "more cores than "
                                                           "you have")
        pool = multiprocessing.Pool(args.cores)
        results = pool.map(remove_taxon_from_alignments, work)
    else:
        results = map(remove_taxon_from_alignments, work)
    print ""
    for f in results:
        if f is not None:
            log.info("Dropped {} because fewer than 1 taxon.".format(f))
    # done
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
