
from __future__ import absolute_import
import os
import re
import sys
import ConfigParser
from Bio import AlignIO

from phyluce.log import setup_logging
from phyluce.common import get_alignment_files, record_formatter


def explode_by_taxon(log, args, files, names):
    log.info("Exploding {} alignments by taxon.".format(len(files)))
    d = {}
    for file in files:
        sys.stdout.write('.')
        sys.stdout.flush()
        basename = os.path.basename(file)
        locus = os.path.splitext(basename)[0]
        aln = AlignIO.read(file, args.input_format)
        for taxon in aln:
            name = re.sub("^(_R_)*{}_*".format(locus), "", taxon.id)
            if name not in args.exclude:
                try:
                    shortname = names[name]
                except:
                    shortname = name
            if shortname not in d.keys():
                new_file = shortname + ".fasta"
                d[shortname] = open(os.path.join(args.output, new_file), 'w')
            new_seq = str(taxon.seq).replace('-', '').replace('?', '')
            if not len(new_seq) == 0:
                new_seq_record = record_formatter(
                    "{} |locus={}".format(shortname, locus),
                    new_seq
                )
                d[shortname].write(new_seq_record.format("fasta"))
    for k, v in d.iteritems():
        v.close()
    print ""


def explode_by_locus(log, args, files, names):
    log.info("Exploding {} alignments by locus.".format(len(files)))
    for file in files:
        sys.stdout.write('.')
        sys.stdout.flush()
        basename = os.path.basename(file)
        locus = os.path.splitext(basename)[0]
        new_file = locus + ".fasta"
        taxon_count = []
        outp = open(os.path.join(args.output, new_file), 'w')
        aln = AlignIO.read(file, args.input_format)
        count = 0
        for taxon in aln:
            name = taxon.id.replace(locus, '').lstrip('_')
            if name not in args.exclude:
                try:
                    shortname = names[name]
                except:
                    shortname = name
                new_seq = str(taxon.seq).replace('-', '').replace('?', '')
                if not len(new_seq) == 0:
                    new_seq_record = record_formatter(
                        "{} |locus={}".format(shortname, locus),
                        new_seq
                    )
                    outp.write(new_seq_record.format("fasta"))
                    count += 1
                else:
                    print locus
        taxon_count.append(count)
        outp.close()
    print ""
    log.info("Final taxon count = {}".format(
        set(taxon_count)
    ))


def main(args, parser):
    # setup logging
    log, my_name = setup_logging(args)
    files = get_alignment_files(
        log,
        args.alignments,
        args.input_format
    )
    try:
        assert len(files) > 0
    except:
        raise IOError("Could not find valid alignment files.  Ensure you are "
                      "Using the correct PATH and setting for --input-format")
    if args.conf:
        conf = ConfigParser.ConfigParser()
        conf.read(args.conf)
        names = {item[0].replace(' ', '_'): item[1]
                 for item in conf.items(args.section)}
        print "Original taxon count = ", len(names.keys())
        for taxon in args.exclude:
            del names[taxon]
    else:
        names = None
    if args.by_taxon:
        explode_by_taxon(log, args, files, names)
    else:
        explode_by_locus(log, args, files, names)
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
