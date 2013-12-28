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
import copy
import ConfigParser
import multiprocessing
from collections import defaultdict
from Bio import AlignIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC, Gapped
from Bio.Align import MultipleSeqAlignment

from phyluce.common import get_alignment_files
from phyluce.log import setup_logging


def get_names_from_config(log, config, group):
    log.info("Getting taxon names from --match-count-output")
    try:
        return [i[0].rstrip('*') for i in config.items(group)]
    except ConfigParser.NoSectionError:
        return None


def record_formatter(seq, name):
    """return a string formatted as a biopython sequence record"""
    return SeqRecord(
        Seq(seq, Gapped(IUPAC.ambiguous_dna, "-?")),
        id=name,
        name=name,
        description=name
    )


def add_gaps_to_align(aln, organisms, missing, verbatim=False, min_taxa=3):
    local_organisms = copy.deepcopy(organisms)
    if len(aln) < min_taxa:
        new_align = None
    elif len(aln) >= min_taxa:
        new_align = MultipleSeqAlignment([], Gapped(IUPAC.ambiguous_dna, "-?"))
        overall_length = len(aln[0])
        for seq in aln:
            # strip any reversal characters from mafft
            seq.name = seq.name.lstrip('_R_')
            if not verbatim:
                new_seq_name = '_'.join(seq.name.split('_')[1:])
            else:
                new_seq_name = seq.name.lower()
            new_align.append(record_formatter(str(seq.seq), new_seq_name))
            local_organisms.remove(new_seq_name)
        for org in local_organisms:
            if not verbatim:
                loc = '_'.join(seq.name.split('_')[:1])
            else:
                loc = seq.name
            if missing:
                try:
                    assert loc in missing[org], "Locus missing"
                except:
                    assert loc in missing['{}*'.format(org)], "Locus missing"
            missing_string = '?' * overall_length
            new_align.append(record_formatter(missing_string, org))
    return new_align


def get_missing_loci_from_conf_file(config):
    missing = defaultdict(list)
    for sec in config.sections():
        for item in config.items(sec):
            missing[sec].append(item[0])
    return missing


def add_designators(work):
    sys.stdout.write('.')
    sys.stdout.flush()
    args, file, organisms, missing = work
    aln = AlignIO.read(file, args.input_format)
    new_align = add_gaps_to_align(
        aln,
        organisms,
        missing,
        args.verbatim,
        args.min_taxa
    )
    if new_align is not None:
        outf = os.path.join(args.output, os.path.basename(file))
        AlignIO.write(new_align, open(outf, 'w'), args.output_format)
        return None
    else:
        return file


def main(args, parser):
    # setup logging
    log, my_name = setup_logging(args)
    # read config file output by match_count_config.py
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(args.match_count_output)
    # read the incomplete matrix file that contains loci that are incomplete
    if args.incomplete_matrix:
        incomplete = ConfigParser.RawConfigParser(allow_no_value=True)
        incomplete.read(args.incomplete_matrix)
        missing = get_missing_loci_from_conf_file(incomplete)
    else:
        missing = None
    # get the taxa in the alignment
    organisms = get_names_from_config(log, config, 'Organisms')
    # get input files
    files = get_alignment_files(log, args.alignments, args.input_format)
    work = [[
            args,
            file,
            organisms,
            missing,
            ] for file in files]
    log.info("Adding missing data designators using {} cores".format(
        args.cores
    ))
    if args.cores > 1:
        assert args.cores <= multiprocessing.cpu_count(), ("You've specified "
                                                           "more cores than "
                                                           "you have")
        pool = multiprocessing.Pool(args.cores)
        results = pool.map(add_designators, work)
    else:
        results = map(add_designators, work)
    print ""
    for result in results:
        if result is not None:
            log.info("Dropped {} because of too few taxa (N < {})".format(
                result,
                args.min_taxa
            ))
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
