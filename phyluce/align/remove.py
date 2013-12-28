#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 28 December 2013 12:12 PST (-0800)
"""

from __future__ import absolute_import
import ConfigParser

from phyluce.common import get_alignment_files
from phyluce.align.common import copy_file
from phyluce.log import setup_logging


def main(args, parser):
    # setup logging
    log, my_name = setup_logging(args)
    # find all alignments
    conf = ConfigParser.ConfigParser()
    conf.optionxform = str
    conf.read(args.config)
    bad_files = [item[0] for item in conf.items(args.section)]
    files = get_alignment_files(
        log,
        args.alignments,
        args.input_format
    )
    log.info("There are {} TOTAL files.".format(len(files)))
    log.info("There are {} BAD files.".format(len(bad_files)))
    expected_copy = len(files) - len(bad_files)
    copied_count, bad_count = copy_file(
        files,
        bad_files,
        args.output,
        expected_copy
    )
    log.info("Copied {} files.  Did not copy {} files.".format(
        copied_count,
        bad_count
    ))
    # end
    text = " Completed {} ".format(my_name)
    log.info(text.center(65, "="))
