#!/usr/bin/env python
# encoding: utf-8
"""
(c) 2014 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.
This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.
Created on 27 April 2014 17:37 PDT (-0700)

Author: Carl Oliveros

Description: Discards loci according to a completeness configuration file.

"""

import os
import sys
import glob
import argparse
import ConfigParser
import random
from multiprocessing import Pool
from Bio.Nexus import Nexus
from Bio.Seq import Seq

from phyluce.helpers import is_dir, FullPaths, CreateDir
from phyluce.log import setup_logging

def get_args():
    parser = argparse.ArgumentParser(
        description='Discards loci according to a completeness configuration file.')
    parser.add_argument(
        "--alignments", 
        required=True,
        type=is_dir, 
        action=FullPaths,
        help="The input directory containing nexus-formatted alignments")
    parser.add_argument(
        "--output-incomplete", 
        required=True,
        action=CreateDir,
        help="The directory in which to store the incomplete alignment files")
    parser.add_argument(
        "--output-complete", 
        required=True,
        action=CreateDir,
        help="The directory in which to store the complete alignment files")
    parser.add_argument(
        "--cores",
        type=int,
        default=1,
        help="""The number of compute cores to use""")
    parser.add_argument(
        "--completeness-conf",
        action=FullPaths,
        type=str,
        help="""A config-formatted file containing full-name:proportion type""")
    parser.add_argument(
        "--log-path",
        action=FullPaths,
        type=is_dir,
        default=None,
        help="The path to a directory to hold logs.")
    parser.add_argument(
        "--verbosity",
        type=str,
        choices=["INFO", "WARN", "CRITICAL"],
        default="INFO",
        help="The logging level to use.")
    return parser.parse_args()    

def generate_exclusion_lists(sampling_map, files):
    exclusion_lists = {}
    for taxon, options in sampling_map.iteritems():
        proportion, mode = options.split()
        if mode == 'r':  
            # randomly choose loci to exclude
            numloci = int((float(proportion))*len(files))
            locus_list = random.sample(files, numloci)
        # insert alternative modes here
        exclusion_lists[taxon] = locus_list
    return exclusion_lists

def filter_files_worker(params):
    f, args, exclusion_lists = params
    delete_taxa = [taxon for taxon in exclusion_lists.keys() if f in exclusion_lists[taxon] ]
    alignment = Nexus.Nexus(f)
    numtaxa = alignment.ntax
    # delete unwanted taxa
    if len(delete_taxa) > 0:
        alignment.matrix = alignment.crop_matrix(delete=delete_taxa)
        alignment.ntax = len(alignment.matrix)
        alignment.taxlabels = alignment.matrix.keys()
    # remove sites with gap/missing data for all taxa
    gaps = alignment.gaponly(include_missing=True)
    if len(gaps) > 0:
        alignment.matrix = alignment.crop_matrix(exclude=gaps)
        taxon = alignment.matrix.keys()[0]
        alignment.nchar = len(alignment.matrix[taxon]._data)
    # write out to incomplete output
    if alignment.ntax > 2:
        new_name = os.path.join(args.output_incomplete,os.path.split(f)[1])
    	alignment.write_nexus_data(new_name)
    # write out to complete output
    if alignment.ntax == numtaxa:
        new_name = os.path.join(args.output_complete,os.path.split(f)[1])
    	alignment.write_nexus_data(new_name)
    # write progress dots
    sys.stdout.write('.')
    sys.stdout.flush()

        
def main():
    args = get_args()
    # setup logging
    log, my_name = setup_logging(args)
    files = glob.glob(os.path.join(os.path.expanduser(args.alignments), '*.nexus'))
    log.info("{} alignments detected in input directory".format(len(files)))
    if len(files) == 0:
        raise IOError("There are no {}-formatted alignments in {}.".format(
            args.input_format,
            args.alignments
        ))    
    # parse completeness config file   
    sampling_config = ConfigParser.ConfigParser()
    sampling_config.readfp(open(args.completeness_conf))
    sampling_map = dict(sampling_config.items('samples'))
    # generate exclusion lists
    exclusion_lists = generate_exclusion_lists(sampling_map, files)
    print(exclusion_lists)
    # filter loci
    params = [[f, args, exclusion_lists] for f in files]
    log.info("Filtering loci")
    if args.cores > 1:
        pool = Pool(args.cores)
        pool.map(filter_files_worker, params)
    else:
        map(filter_files_worker, params)
    print ""
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
        
if __name__ == '__main__':
    main()