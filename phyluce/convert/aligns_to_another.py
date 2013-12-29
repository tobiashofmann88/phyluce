#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 29 December 2013 09:43 PST (-0800)
"""

from __future__ import absolute_import
import os
import sys
import ConfigParser
from multiprocessing import Pool

from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment as Alignment
from Bio.Alphabet import IUPAC, Gapped

from phyluce.log import setup_logging
from phyluce.common import get_alignment_files


def test_if_name_in_keys(name, keys):
    if name in keys:
        for i in xrange(100):
            name = "{0}{1}".format(name, i)
            if name not in keys:
                break
            else:
                continue
    return name


def shorten_name(args, aln):
    aln = AlignIO.read(aln, args.input_format)
    names = {}
    for seq in aln:
        if "-" in seq.id:
            split_name = seq.id.split("-")
        elif "_" in seq.id:
            split_name = seq.id.split("_")
        elif " " in seq.id:
            split_name = seq.id.split(" ")
        else:
            split_name = None
        if split_name is not None:
            f3, l3 = split_name[0][0:3].title(), split_name[1][0:3].title()
            new_name = "{0}{1}".format(f3, l3)
        else:
            new_name = seq.id[:6]
        new_name = test_if_name_in_keys(new_name, names.keys())
        names[seq.id] = new_name
        seq.id, seq.name = new_name, new_name
    return names


def rename_alignment_taxa(aln, name_map):
    new_align = Alignment([], alphabet=Gapped(IUPAC.unambiguous_dna, "-"))
    for seq in aln:
        seq.id, seq.name = name_map[seq.id], name_map[seq.id]
        new_align.append(seq)
    return new_align


def convert_files_worker(params):
    f, args, name_map = params
    aln = AlignIO.read(
        f,
        args.input_format,
        alphabet=Gapped(IUPAC.ambiguous_dna)
    )
    if args.shorten_name:
        aln = rename_alignment_taxa(aln, name_map)
    new_name = os.path.splitext(os.path.split(f)[1])[0] + '.{0}'.format(
        args.output_format
    )
    outf = open(os.path.join(args.output, new_name), 'w')
    try:
        AlignIO.write(aln, outf, args.output_format)
    except ValueError as e:
        if (args.output_format == "phylip" and
                e.message.startswith("Repeated name")):
            raise IOError("Your sequence names are too long for PHYLIP format. "
                          "You need to use --shorten-names, --input-format="
                          "phylip-relaxed, or --name-conf with a correct "
                          "mapping of long names to short (< 10 character) "
                          "names.")
        else:
            raise
    except:
        raise
    outf.close()
    sys.stdout.write('.')
    sys.stdout.flush()


def main(args, parser):
    # setup logging
    log, my_name = setup_logging(args)
    files = get_alignment_files(
        log,
        args.alignments,
        args.input_format
    )
    if args.shorten_name and not args.name_conf:
        log.info("Determining short names")
        name_map = shorten_name(args, files[0])
    elif args.shorten_name and args.name_conf:
        log.info("Getting names from config file")
        conf = ConfigParser.ConfigParser()
        conf.readfp(open(args.name_conf))
        name_map = dict(conf.items('taxa'))
    else:
        name_map = None
    params = [[f, args, name_map] for f in files]
    log.info('Converting {} alignments of format={} to format={}'.format(
        len(files),
        args.input_format,
        args.output_format
    ))
    if args.cores > 1:
        pool = Pool(args.cores)
        pool.map(convert_files_worker, params)
    else:
        map(convert_files_worker, params)
    print ""
    if args.shorten_name:
        log.info(
            "\n\nTaxa renamed (from) => (to):"
        )
        for k, v in name_map.iteritems():
            log.info(
                "\t{0} => {1}".format(k, v)
            )
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
