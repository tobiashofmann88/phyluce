#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2013 Brant Faircloth || http://faircloth-lab.org/
All rights reserved.

This code is distributed under a 3-clause BSD license. Please see
LICENSE.txt for more information.

Created on 29 December 2013 17:25 PST (-0800)
"""

import os
import pytest
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
    # content of test_class.py
    def test_mafft(self, conda_dir):
        expected_mafft = os.path.join(
            conda_dir,
            "mafft"
        )
        assert which("mafft") == expected_mafft

    # content of test_class.py
    def test_velvetg(self, conda_dir):
        expected_velvet = os.path.join(
            conda_dir,
            "velvetg"
        )
        assert which("velvetg") == expected_velvet

    # content of test_class.py
    def test_velveth(self, conda_dir):
        expected_velvet = os.path.join(
            conda_dir,
            "velveth"
        )
        assert which("velveth") == expected_velvet

    # content of test_class.py
    def test_abyss_pe(self, conda_dir):
        expected_abyss = os.path.join(
            conda_dir,
            "abyss-pe"
        )
        assert which("abyss-pe") == expected_abyss

    # content of test_class.py
    def test_abyss(self, conda_dir):
        expected_abyss = os.path.join(
            conda_dir,
            "ABYSS"
        )
        assert which("ABYSS") == expected_abyss
