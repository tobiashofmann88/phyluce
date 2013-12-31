#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 29 December 2013 17:25 PST (-0800)
"""

from __future__ import absolute_import
import os
import pytest
import subprocess
from phyluce.common import which


@pytest.fixture(scope="module")
def conda_dir():
    try:
        if os.environ["CONDA_DEFAULT_ENV"] is not "":
            return os.path.join(
                os.path.expandvars("$HOME"),
                "anaconda",
                "envs",
                os.environ["CONDA_DEFAULT_ENV"],
                "bin"
            )
    except KeyError:
        return os.path.join(
            os.path.expandvars("$HOME"),
            "anaconda/bin"
        )


class TestWhichBinary:
    """Test that the binaries are in their proper place for anaconda"""
    def test_mafft(self, conda_dir):
        expected_mafft = os.path.join(
            conda_dir,
            "mafft"
        )
        assert which("mafft") == expected_mafft

    def test_velvetg(self, conda_dir):
        expected_velvet = os.path.join(
            conda_dir,
            "velvetg"
        )
        assert which("velvetg") == expected_velvet

    def test_velveth(self, conda_dir):
        expected_velvet = os.path.join(
            conda_dir,
            "velveth"
        )
        assert which("velveth") == expected_velvet

    def test_abyss_pe(self, conda_dir):
        expected_abyss = os.path.join(
            conda_dir,
            "abyss-pe"
        )
        assert which("abyss-pe") == expected_abyss

    def test_abyss(self, conda_dir):
        expected_abyss = os.path.join(
            conda_dir,
            "ABYSS"
        )
        assert which("ABYSS") == expected_abyss


class TestBinaryFunction:
    """Test that the binaries actually do something"""
    def test_mafft(self, conda_dir):
        cmd = ["mafft", "-v"]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        assert stdout == ""
        assert stderr == ""
        observed_mafft = stderr.split("\n")[3].lstrip()
        expected_mafft = 'MAFFT v7.130b (2013/12/05)'
        assert observed_mafft == expected_mafft

    def test_velveth(self, conda_dir):
        cmd = ["velveth"]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        observed_velveth = stdout.split("\n")[1]
        expected_velveth = 'Version 1.2.10'
        assert observed_velveth == expected_velveth

    def test_velvetg(self, conda_dir):
        cmd = ["velvetg"]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        observed_velvetg = stdout.split("\n")[1]
        expected_velvetg = 'Version 1.2.10'
        assert observed_velvetg == expected_velvetg

    def test_ABYSS(self, conda_dir):
        cmd = ["ABYSS", "--version"]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        observed_ABYSS = stdout.split("\n")[0]
        expected_ABYSS = 'ABYSS (ABySS) 1.3.7'
        assert observed_ABYSS == expected_ABYSS
