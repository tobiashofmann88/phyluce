from __future__ import absolute_import
from phyluce.core import helpers
from phyluce.cli import sub_assemble_velvet
from phyluce.cli import sub_assemble_abyss


descr = "Methods to assemble cleaned sequencing reads."

def configure_parser(sub_parsers):
    p = sub_parsers.add_parser('assemble', description=descr, help=descr)

    sub_parsers = p.add_subparsers(
        metavar = "command",
        dest = "cmd",
    )

    sub_assemble_velvet.configure_parser(sub_parsers)
    sub_assemble_abyss.configure_parser(sub_parsers)
