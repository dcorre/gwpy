# -*- coding: utf-8 -*-
# Copyright (C) Duncan Macleod (2013)
#
# This file is part of GWpy.
#
# GWpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GWpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GWpy.  If not, see <http://www.gnu.org/licenses/>.

"""Unit tests for :mod:`gwpy.io.utils`
"""

import gzip
import os.path
import tempfile

from six import PY2

from .. import utils as io_utils

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'


def test_gopen():
    # test simple use
    try:
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as f:
            f.write('blah blah blah')
        f2 = io_utils.gopen(f.name)
        assert f2.read() == 'blah blah blah'
    finally:
        if os.path.isfile(f.name):
            os.remove(f.name)

    # test gzip file (with and without extension)
    for suffix in ('.txt.gz', ''):
        try:
            fn = tempfile.mktemp(suffix=suffix)
            text = 'blah blah blah' if PY2 else b'blah blah blah'
            with gzip.open(fn, 'wb') as f:
                f.write(text)
            f2 = io_utils.gopen(fn, mode='rb')
            assert isinstance(f2, gzip.GzipFile)
            assert f2.read() == text
        finally:
            if os.path.isfile(fn):
                os.remove(f.name)


def test_identify_factory():
    id_func = io_utils.identify_factory('.blah', '.blah2')
    assert id_func(None, None, None) is False
    assert id_func(None, 'test.txt', None) is False
    assert id_func(None, 'test.blah', None) is True
    assert id_func(None, 'test.blah2', None) is True
    assert id_func(None, 'test.blah2x', None) is False