#!/usr/bin/env python
# encoding: utf-8
"""
(c) 2014 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.
This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.
Created on 27 April 2014 17:37 PDT (-0700)

Author: Carl Oliveros

Description: Prunes sequence data from alignments according to a completeness configuration file.

"""

import os
import sys
import glob
import argparse
import ConfigParser
import random
import numpy
import math
import shutil
from multiprocessing import Pool
from Bio.Nexus import Nexus
from Bio.Seq import Seq

from phyluce.helpers import is_dir, FullPaths, CreateDir
from phyluce.log import setup_logging

def get_args():
    parser = argparse.ArgumentParser(
        description='Prunes sequence data from alignments according to a completeness configuration file.')
    parser.add_argument(
        "--alignments", 
        required=True,
        type=is_dir, 
        action=FullPaths,
        help="The input directory containing nexus-formatted alignments")
    parser.add_argument(
        "--output-prefix", 
        required=True,
        help="The prefix to use for directories in which to store the incomplete alignment files")
    parser.add_argument(
        "--completeness-levels", 
        nargs='+',
        type=str,
        default=['75','100'],
        help="Proportions of taxa that must be present in each locus.  Default=[75, 100]")
    parser.add_argument(
        "--cores",
        type=int,
        default=1,
        help="""The number of compute cores to use""")
    parser.add_argument(
        "--completeness-conf",
        action=FullPaths,
        required=True,
        type=str,
        help="""A config-formatted file containing full name:proportion type, under heading [samples]""")
    parser.add_argument(
        "--probability-matrix",
        action=FullPaths,
        type=str,
        help="""A config-formatted file containing uce name:propability of enrichment, under heading [probs]""")
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

def create_dir(directory):
    # get the full path
    d = os.path.abspath(os.path.expanduser(directory))
    # check to see if directory exists
    if os.path.exists(d):
        answer = raw_input("[WARNING] Output directory {} exists, REMOVE [Y/n]? ".format(d))
        if answer == "Y":
            shutil.rmtree(d)
        else:
            print "[QUIT]"
            sys.exit()
    # create the new directory
    os.makedirs(d)
    return d


def generate_exclusion_lists(sampling_map, files, args):
    exclusion_lists = {}
    for taxon, options in sampling_map.iteritems():
        proportion, mode = options.split()
        if mode == 'r':  
            # randomly choose loci to exclude
            numloci = int((float(proportion))*len(files))
            locus_list = random.sample(files, numloci)
        if mode == 'u':  
            # choose loci to exclude according to probability matrix
            locus_list = []
            # loci to be discarded
            numloci = int((float(proportion))*len(files))
            # read locus probabilities
            prob_config = ConfigParser.ConfigParser()
            prob_config.readfp(open(args.probability_matrix))
            prob_matrix = dict(prob_config.items('probs'))
            while len(locus_list) < numloci:
                candidate = random.choice(files)
                if candidate not in locus_list:
                    candidate_name = os.path.splitext(os.path.basename(candidate))[0]
                    if numpy.random.binomial(1, 1 - float(prob_matrix[candidate_name])):
                        locus_list.append(candidate) 
        # insert alternative modes here
        exclusion_lists[taxon] = locus_list
    return exclusion_lists

def filter_files_worker(params):
    f, args, exclusion_lists, output_dirs = params
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
    # write alignments to output directories
    for prop in args.completeness_levels:
    	min_taxa = int(math.ceil(numtaxa * float(prop) / 100))
        if alignment.ntax >= min_taxa:
            new_name = os.path.join(output_dirs[prop],os.path.split(f)[1])
            alignment.write_nexus_data(new_name)
    # write progress dots
    sys.stdout.write('.')
    sys.stdout.flush()

        
def main():
    args = get_args()
    # setup logging
    log, my_name = setup_logging(args)
    # create output directories
    output_dirs = {}
    for prop in args.completeness_levels:
        output_dirs[prop] = create_dir(args.output_prefix + "_" + prop + "_nexus")
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
    log.info("Generating exclusion lists")
    exclusion_lists = generate_exclusion_lists(sampling_map, files, args)
    # filter loci
    params = [[f, args, exclusion_lists, output_dirs] for f in files]
    log.info("Filtering loci")
    if args.cores > 1:
        pool = Pool(args.cores)
        pool.map(filter_files_worker, params)
    else:
        map(filter_files_worker, params)
    print ""
    for prop in args.completeness_levels:
        files = glob.glob(os.path.join(output_dirs[prop], '*.nexus'))
    	log.info("{0} alignments written to {1} complete matrix".format(len(files), prop))    
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
        
if __name__ == '__main__':
    main()