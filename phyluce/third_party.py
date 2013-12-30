#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 29 December 2013 16:41 PST (-0800)
"""

from __future__ import absolute_import
import subprocess


def which(prog):
    cmd = ["which", prog]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate()
    if stderr:
        raise EnvironmentError("Program {} does not appear to be installed")
    else:
        return stdout.strip()
