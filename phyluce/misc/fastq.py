#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 29 December 2013 14:04 PST (-0800)
"""

from __future__ import absolute_import
import os
import sys
import numpy
import tempfile
import subprocess
import multiprocessing

from phyluce.log import setup_logging
from phyluce.common import get_fastq_files


def get_fastq_dirs(log, args):
    all_files = {}
    for root, dirs, files in os.walk(args.fastqs, topdown=False):
        if args.exclude:
            for ex in args.exclude:
                dirs.remove(ex)
        # get any fastqs in the root dir
        fastqs = get_fastq_files(log, root)
        if not args.by_file:
            if fastqs:
                all_files[root] = fastqs
        else:
            if fastqs:
                for fastq in fastqs:
                    all_files[fastq] = [fastq]
        # now recurse into subdirs looking for fastqs
        for dir in dirs:
            pth = os.path.join(root, dir)
            fastqs = get_fastq_files(log, pth)
            if not args.by_file:
                if fastqs:
                    all_files[pth] = fastqs
            else:
                if fastqs:
                    for fastq in fastqs:
                        all_files[fastq] = [fastq]
    return all_files


def fastq_worker(work):
    dir, fastqs = work
    fd, templen = tempfile.mkstemp(suffix='.fqcount')
    os.close(fd)
    templen_stdout = open(templen, 'w')
    for f in fastqs:
        if f.endswith('.gz'):
            # not secure
            cmd = ("gunzip -c {} | "
                   "awk '{{if(NR%4==2) print length($1)}}'").format(f)
        else:
            # not secure
            cmd = ("cat {} | "
                   "awk '{{if(NR%4==2) print length($1)}}'").format(f)
        proc = subprocess.Popen(
            cmd,
            stdout=templen_stdout,
            stderr=subprocess.PIPE,
            shell=True
        )
        stdout, stderr = proc.communicate()
        sys.stdout.write('.')
        sys.stdout.flush()
    templen_stdout.close()
    if stderr == '':
        lengths = [int(l.strip()) for l in open(templen, 'rU')]
    os.remove(templen)
    lengths = numpy.array(lengths)
    std_error = numpy.std(lengths, ddof=1) / numpy.sqrt(len(lengths))
    return (lengths, std_error, dir)


def main(args, parser):
    # setup logging
    log, my_name = setup_logging(args)
    fastq_files = get_fastq_dirs(log, args)
    work = [(k, v) for k, v in fastq_files.iteritems()]
    log.info("Getting FASTA stats using {} cores".format(args.cores))
    if args.cores > 1:
        assert args.cores <= multiprocessing.cpu_count(), ("You've specified "
                                                           "more cores than "
                                                           "you have")
        pool = multiprocessing.Pool(args.cores)
        results = pool.map(fastq_worker, work)
    else:
        results = map(fastq_worker, work)
    print ""
    if len(results) == 1 and not args.output and not args.csv:
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
    elif not args.output and ((len(results) == 1 and args.csv)
                              or (len(results) > 1)):
        log.info("file,reads,bp,avg_len,stderr_len,min_len,max_len,median_len")
        for r in results:
            r0, r1, r2 = r
            log.info("{},{},{},{},{},{},{},{}".format(
                os.path.basename(r2),
                len(r0),
                sum(r0),
                numpy.average(r0),
                r1,
                min(r0),
                max(r0),
                numpy.median(r0)
            ))
    elif args.output:
        log.info("Writing CSV results to {}".format(args.output))
        with open(args.output, 'w') as outf:
            outf.write("file,reads,bp,avg_len,stderr_len,min_len,max_len,"
                       "median_len\n")
            for r0, r1, r2 in results:
                outf.write("{},{},{},{},{},{},{},{}".format(
                    os.path.basename(r2),
                    len(r0),
                    sum(r0),
                    numpy.average(r0),
                    r1,
                    min(r0),
                    max(r0),
                    numpy.median(r0)
                ))
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
