
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 28 December 2013 15:12 PST (-0800)
"""


from __future__ import absolute_import
import os
import re
import sys
import itertools
import multiprocessing

from Bio import AlignIO
from Bio.Alphabet import generic_dna
from Bio.Align import MultipleSeqAlignment

from phyluce.log import setup_logging
from phyluce.common import get_alignment_files


def clean_files(work):
    sys.stdout.write('.')
    sys.stdout.flush()
    f, args = work
    all_taxa = set([])
    new_align = MultipleSeqAlignment([], generic_dna)
    for align in AlignIO.parse(f, args.input_format):
        for seq in list(align):
            fname = os.path.splitext(os.path.basename(f))[0]
            new_seq_name = re.sub(
                "^(_R_)*{}_*".format(fname),
                "",
                seq.name
            )
            all_taxa.add(new_seq_name)
            seq.id = new_seq_name
            seq.name = new_seq_name
            new_align.append(seq)
        if args.taxa is not None:
            try:
                assert len(all_taxa) == args.taxa
            except:
                raise IOError("There appear to be more than the maximum "
                              "number of taxa")
        try:
            output_name = os.path.join(args.output, os.path.split(f)[1])
            with open(output_name, 'w') as outf:
                AlignIO.write(new_align, outf, args.output_format)
        except ValueError:
            raise IOError("Cannot write output file.")
    return all_taxa


def main(args, parser):
    # setup logging
    log, my_name = setup_logging(args)
    files = get_alignment_files(
        log,
        args.alignments,
        args.input_format
    )
    log.info("Cleaning {} alignment files".format(len(files)))
    work = [(f, args) for f in files]
    log.info("Cleaning alignments using {} cores".format(args.cores))
    if args.cores > 1:
        assert args.cores <= multiprocessing.cpu_count(), ("You've specified "
                                                           "more cores than "
                                                           "you have")
        pool = multiprocessing.Pool(args.cores)
        taxa = pool.map(clean_files, work)
    else:
        taxa = map(clean_files, work)
    print ""
    all_taxa = set(list(itertools.chain.from_iterable(taxa)))
    log.info("Taxon names in alignments: {0}".format(','.join(list(all_taxa))))
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
