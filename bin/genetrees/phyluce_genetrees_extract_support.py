#!/usr/bin/env python
# encoding: utf-8
"""
(c) 2014 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.
This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.
Created on 27 April 2014 17:37 PDT (-0700)

Author: Carl Oliveros

Description: Extracts support values for nodes and directories specified in a config file.

"""

import os
import sys
import glob
import argparse
import ConfigParser
import dendropy

from phyluce.helpers import is_dir, FullPaths
from phyluce.log import setup_logging

def get_args():
    parser = argparse.ArgumentParser(
        description='Extracts support values for nodes and directories specified in a config file.')
    parser.add_argument(
        "--config",
        action=FullPaths,
        required=True,
        type=str,
        help="""A config-formatted file containing nodes, directories and filenames""")
    parser.add_argument(
        "--output", 
        required=True,
        type=str,
        action=FullPaths,
        help="The filename in which to store output")
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


def rchop(name, ending):
    if name.endswith(ending):
        return name[:-len(ending)]
    return name


def read_config(conf):
    # read config file
    config_file = ConfigParser.RawConfigParser(allow_no_value=True)
    config_file.optionxform = str
    config_file.readfp(open(conf))
    # retrieve nodes
    nodes = dict(config_file.items('nodes'))
    for nd in nodes.keys():
        nodes[nd] = nodes[nd].split
    # retrieve directories
    directories = config_file.options('directories')
    # retrieve filenames
    filenames = dict(config_file.items('filenames'))
    return nodes, directories, filenames
        
        
def main():
    args = get_args()
    # setup logging
    log, my_name = setup_logging(args)
    nodes, directories, filenames = read_config(args.config)
    dirs = sorted(directories)
    node_names = sorted(nodes.keys())
    outf = open(args.output, 'w')
    header = '\t' + '\t'.join(node_names) + '\n'
    outf.write(header)
    for method in sorted(filenames.keys()):
        outf.write('{}\n'.format(method))
        for dir in dirs:
            short_dir = rchop(os.path.basename(dir), "_speciestree")
            outf.write('{}\t'.format(short_dir))
            files = glob.glob(os.path.join(dir, filenames[method]))
            trees = dendropy.TreeList()
            for f in files:
                trees.read_from_path(f,'newick')
            for nd in node_names:
                print(nodes[nd])            
                freq = trees.frequency_of_split(labels=nodes[nd])
                outf.write('{}\t'.format(freq))
            outf.write('\n')
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
        
if __name__ == '__main__':
    main()