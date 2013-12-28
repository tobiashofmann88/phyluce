#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 27 December 2013 15:12 PST (-0800)
"""

from __future__ import absolute_import
import os
import sys
import copy
import shutil
import tempfile
import multiprocessing
from Bio import SeqIO
from collections import defaultdict

from phyluce.common import write_alignments_to_outdir
from phyluce.log import setup_logging


def copy_file(files, bad_files, output, expected_copy):
    copied_count = 0
    bad_count = 0
    for file in files:
        fname = os.path.basename(file)
        if fname not in bad_files:
            outpath = os.path.join(output, fname)
            copied_count += 1
            shutil.copy(file, outpath)
        else:
            bad_count += 1
    try:
        assert expected_copy == copied_count
    except:
        raise IOError("Copied a different number of files than expected")
    return copied_count, bad_count


def build_locus_dict(log, loci, locus, record, ambiguous=False):
    if not ambiguous:
        if not "N" in record.seq:
            loci[locus].append(record)
        else:
            log.warn("Skipping {} because it contains"
                     " ambiguous bases".format(locus))
    else:
        loci[locus].append(record)
    return loci


def create_locus_specific_fasta(sequences):
    fd, fasta_file = tempfile.mkstemp(suffix=".fasta")
    for seq in sequences:
        os.write(fd, seq.format("fasta"))
    os.close(fd)
    return fasta_file


def align(params):
    locus, opts = params
    name, sequences = locus
    # get additional params from params tuple
    window, threshold, notrim, proportion, divergence, min_len, Engine = opts
    fasta = create_locus_specific_fasta(sequences)
    aln = Engine(fasta)
    aln.run_alignment()
    if notrim:
        aln.trim_alignment(
            method="notrim"
        )
    else:
        aln.trim_alignment(
            method="running",
            window_size=window,
            proportion=proportion,
            threshold=threshold,
            max_divergence=divergence,
            min_len=min_len
        )
    if aln.trimmed:
        sys.stdout.write(".")
    else:
        sys.stdout.write("X")
    sys.stdout.flush()
    return (name, aln)


def get_fasta_dict(log, args):
    log.info("Building the locus dictionary")
    if args.ambiguous:
        log.info("NOT removing sequences with ambiguous bases...")
    else:
        log.info("Removing ALL sequences with ambiguous bases...")
    loci = defaultdict(list)
    with open(args.fasta, "rU") as infile:
        for record in SeqIO.parse(infile, "fasta"):
            locus = record.description.split("|")[1]
            loci = build_locus_dict(log, loci, locus, record, args.ambiguous)
    # workon a copy so we can iterate and delete
    snapshot = copy.deepcopy(loci)
    # iterate over loci to check for all species at a locus
    for locus, data in snapshot.iteritems():
        if args.notstrict:
            if len(data) < 3:
                del loci[locus]
                log.warn("DROPPED locus {0}. "
                         "Too few taxa (N < 3).".format(locus))
        else:
            if len(data) < args.taxa:
                del loci[locus]
                log.warn("DROPPED locus {0}. Alignment does not "
                         "contain all {1} taxa.".format(locus, args.taxa))
    return loci


def main(args, parser, engine):
    # setup logging
    log, my_name = setup_logging(args)
    # create the fasta dictionary
    loci = get_fasta_dict(log, args)
    log.info("Aligning with {}".format(str(args.aligner).upper()))
    opts = [[args.window, args.threshold, args.no_trim, args.proportion,
             args.max_divergence, args.min_length, engine]
            for i in range(len(loci))]
    # combine loci and options
    params = zip(loci.items(), opts)
    log.info("Alignment begins. 'X' indicates dropped alignments "
             "(these are reported after alignment)")
    # During alignment, drop into sys.stdout for progress indicator
    # because logging in multiprocessing is more painful than what
    # we really need.  Return to logging when alignment completes.
    if args.cores > 1:
        assert args.cores <= multiprocessing.cpu_count(), ("You've specified "
                                                           "more cores than "
                                                           "you have")
        pool = multiprocessing.Pool(args.cores)
        alignments = pool.map(align, params)
    else:
        alignments = map(align, params)
    # kick the stdout down one line since we were using sys.stdout
    print("")
    # drop back into logging
    log.info("Alignment ends")
    # write the output files
    write_alignments_to_outdir(
        log,
        args.output,
        alignments,
        args.output_format
    )
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
