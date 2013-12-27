from __future__ import absolute_import
from phyluce.core import helpers


descr = "Assemble reads using abYss."


def configure_parser(sub_parsers):
    p = sub_parsers.add_parser('abyss', description=descr, help=descr)


    p.set_defaults(func=execute)


def execute(args, parser):
    pass
