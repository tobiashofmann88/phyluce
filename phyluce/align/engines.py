#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 27 December 2013 15:12 PST (-0800)
"""

from __future__ import absolute_import
import os
import tempfile
import subprocess

from Bio import AlignIO
from Bio.Alphabet import IUPAC, Gapped

from phyluce.common import which
from phyluce.align.generic import GenericAlign

#import pdb


class Mafft(GenericAlign):
    """ MAFFT alignment class.  Subclass of GenericAlign which
    contains a majority of the alignment-related helper functions
    (trimming, etc.) """

    def __init__(self, input):
        """initialize, calling superclass __init__ also"""
        super(Align, self).__init__(input)

    def run_alignment(self, clean=True):
        mafft = which("mafft")
        # create results file
        fd, aln = tempfile.mkstemp(suffix='.mafft')
        os.close(fd)
        aln_stdout = open(aln, 'w')
        # run MAFFT on the temp file
        cmd = [mafft, "--adjustdirection", "--maxiterate", "1000", self.input]
        # just pass all ENV params
        proc = subprocess.Popen(cmd,
                stderr=subprocess.PIPE,
                stdout=aln_stdout
            )
        stderr = proc.communicate()
        aln_stdout.close()
        self.alignment = AlignIO.read(open(aln, 'rU'), "fasta", \
                alphabet=Gapped(IUPAC.unambiguous_dna, "-"))
        if clean:
            self._clean(aln)


class Muscle(GenericAlign):
    """ MUSCLE alignment class.  Subclass of GenericAlign which
    contains a majority of the alignment-related helper functions
    (trimming, etc.) """

    def __init__(self, input):
        """initialize, calling superclass __init__ also"""
        super(Align, self).__init__(input)

    def run_alignment(self, clean=True):
        """ muscle """
        # dialign requires ENV variable be set for dialign_dir
        muscle = which("muscle")
        # create results file
        fd, aln = tempfile.mkstemp(suffix='.muscle')
        os.close(fd)
        # run MUSCLE on the temp file
        cmd = [muscle, "-in", self.input, "-out", aln]
        proc = subprocess.Popen(cmd,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE
            )
        stdout, stderr = proc.communicate()
        self.alignment = AlignIO.read(open(aln, 'rU'), \
                "fasta", alphabet=Gapped(IUPAC.unambiguous_dna, "-"))
        # cleanup temp files
        if clean:
            self._clean(aln)
