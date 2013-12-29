#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 29 December 2013 13:07 PST (-0800)
"""

from __future__ import absolute_import
import os
import gzip
import numpy
import multiprocessing
from itertools import groupby

from phyluce.log import setup_logging
from phyluce.common import get_fasta_files


def fasta_iter(fasta):
    """
    modified from @brent_p on stackoverflow.  yield tuple of header,
    sequence
    """
    if fasta.endswith('.gz'):
        with gzip.open(fasta) as f:
            faiter = (x[1] for x in groupby(f, lambda line: line[0] == ">"))
            for header in faiter:
                yield sum(len(s.strip()) for s in faiter.next())
    else:
        with open(fasta) as f:
            faiter = (x[1] for x in groupby(f, lambda line: line[0] == ">"))
            for header in faiter:
                yield sum(len(s.strip()) for s in faiter.next())


def fasta_worker(fasta):
    lengths = numpy.array([int(record) for record in fasta_iter(fasta)])
    std_error = numpy.std(lengths, ddof=1) / numpy.sqrt(len(lengths))
    return (lengths, std_error, os.path.basename(fasta))


def main(args, parser):
    # setup logging
    log, my_name = setup_logging(args)
    if os.path.isfile(args.fastas):
        log.info("Getting FASTA file")
        single_file = True
        work = [args.fastas]
    elif os.path.isdir(args.fastas):
        # prints own log info stmnt
        single_file = False
        files = get_fasta_files(
            log,
            args.fastas,
        )
        work = files
    log.info("Getting FASTA stats using {} cores".format(args.cores))
    if args.cores > 1:
        assert args.cores <= multiprocessing.cpu_count(), ("You've specified "
                                                           "more cores than "
                                                           "you have")
        pool = multiprocessing.Pool(args.cores)
        results = pool.map(fasta_worker, work)
    else:
        results = map(fasta_worker, work)
    results = map(fasta_worker, work)
    if single_file and not args.output and not args.csv:
        for r in results:
            r0, r1, r2 = r
            template = "{0:15}{1:,}"
            log.info(template.format("Reads", len(r0)))
            log.info(template.format("bp", sum(r0)))
            log.info(template.format("AVG len.", numpy.average(r0)))
            log.info(template.format("STDERR len.", r1))
            log.info(template.format("MIN len.", min(r0)))
            log.info(template.format("MAX len.", max(r0)))
            log.info(template.format("MEDIAN len.", numpy.median(r0)))
            log.info(template.format("Contigs > 1kb", sum(r0 >= 1000)))
    elif not args.output and ((single_file and args.csv) or (not single_file)):
        log.info("file,reads,bp,avg_len,stderr_len,min_len,max_len,median_len,"
                 "contigs>1kb")
        for r in results:
            r0, r1, r2 = r
            log.info("{},{},{},{},{},{},{},{},{}".format(
                os.path.basename(r2),
                len(r0),
                sum(r0),
                numpy.average(r0),
                r1,
                min(r0),
                max(r0),
                numpy.median(r0),
                sum(r0 >= 1000)
            ))
    elif args.output:
        log.info("Writing CSV results to {}".format(args.output))
        with open(args.output, 'w') as outf:
            outf.write("file,reads,bp,avg_len,stderr_len,min_len,max_len,"
                       "median_len,contigs>1kb\n")
            for r0, r1, r2 in results:
                outf.write("{},{},{},{},{},{},{},{},{}".format(
                    os.path.basename(r2),
                    len(r0),
                    sum(r0),
                    numpy.average(r0),
                    r1,
                    min(r0),
                    max(r0),
                    numpy.median(r0),
                    sum(r0 >= 1000)
                ))
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
