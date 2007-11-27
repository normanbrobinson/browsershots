# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
Managing screenshots as PNG files.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import re
import os
import tempfile
from xmlrpclib import Fault
from django.conf import settings
from shotserver04.nonces import crypto

ORIGINAL_SIZE = 'original'
HEADER_MATCH = re.compile(r'(\S\S)\s+(\d+)\s+(\d+)\s+').match


def png_path(hashkey, size=ORIGINAL_SIZE):
    """Get the full filesystem path for a PNG directory."""
    return os.path.join(settings.PNG_ROOT, str(size), hashkey[:2])


def png_filename(hashkey, size=ORIGINAL_SIZE):
    """Get the full filesystem path for a PNG file."""
    return os.path.join(png_path(hashkey, size), hashkey + '.png')


def makedirs(path):
    """
    Make directory (and parents) if necessary.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def save_upload(screenshot):
    """
    Save uploaded screenshot file and return hashkey.
    """
    hashkey = crypto.random_md5()
    makedirs(png_path(hashkey))
    outfile = file(png_filename(hashkey), 'wb')
    outfile.write(screenshot.data)
    outfile.close()
    return hashkey


def pngtoppm(hashkey):
    """
    Decode PNG file and return temporary PPM filename.
    """
    pngname = png_filename(hashkey)
    ppmhandle, ppmname = tempfile.mkstemp()
    os.close(ppmhandle)
    error = os.system('pngtopnm "%s" > "%s"' % (pngname, ppmname))
    if error:
        makedirs(png_path(hashkey, 'error'))
        errorname = png_filename(hashkey, 'error')
        os.system('mv "%s" "%s"' % (pngname, errorname))
        raise Fault(415,
            "Could not decode uploaded PNG file (hashkey %s)." % hashkey)
    if not os.path.exists(ppmname):
        raise Fault(500, "Decoded screenshot file not found.")
    if os.path.getsize(ppmname) == 0:
        raise Fault(500, "Decoded screenshot file is empty.")
    return ppmname


def read_pnm_header(ppmname):
    """
    Try to read PNM header from decoded screenshot.
    """
    header = file(ppmname, 'rb').read(1024)
    match = HEADER_MATCH(header)
    if match is None:
        raise Fault(500,
            "Could not read PNM header after decoding uploaded PNG file.")
    return (
        match.group(1),
        int(match.group(2)),
        int(match.group(3)),
        )


def scale(ppmname, width, hashkey):
    """
    Make small preview image from uploaded screenshot.
    """
    makedirs(png_path(hashkey, size=width))
    pngname = png_filename(hashkey, size=width)
    error = os.system('pnmscale -width=%d "%s" | pnmtopng > %s' %
                      (width, ppmname, pngname))
    if error:
        raise Fault(500,
            "Could not create scaled preview image.")
