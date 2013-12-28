#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 26 December 2013 16:12 PST (-0800)
"""

from __future__ import absolute_import
import sys
import argparse

from phyluce.cli import main_help
from phyluce.cli import main_assemble
from phyluce.cli import main_fetch
from phyluce.cli import main_align


def main():
    # print same output as help if no arguments
    if len(sys.argv) == 1:
        sys.argv.append("-h")
    # setup main program args
    p = argparse.ArgumentParser(
        description="phyluce is a software package for processing UCE"
                    "and other phylogenomic data for systematics and"
                    "population genetics."
    )
    p.add_argument(
        "-V", "--version",
        action="version",
        version="phyluce {}".format("2.0.0")
    )

    sub_parsers = p.add_subparsers(
        metavar="command",
        dest="cmd",
    )

    main_help.configure_parser(sub_parsers)
    main_assemble.configure_parser(sub_parsers)
    main_fetch.configure_parser(sub_parsers)
    main_align.configure_parser(sub_parsers)
    #main_stats.configure_parser(sub_parsers)
    #main_clean.configure_parser(sub_parsers)
    #main_convert.configure_parser(sub_parsers)

    try:
        import argcomplete
        argcomplete.autocomplete(p)
    except ImportError:
        pass
    except AttributeError:
        # On Python 3.3, argcomplete can be an empty namespace package when
        # argcomplete is not installed. Not sure why, but this fixes it.
        pass

    args = p.parse_args()

    try:
        args.func(args, p)
    except RuntimeError as e:
        sys.exit("Error: %s" % e)
    except Exception as e:
        raise


if __name__ == "__main__":
    main()
