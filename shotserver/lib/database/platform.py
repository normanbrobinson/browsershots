# -*- coding: utf-8 -*-
# browsershots.org
# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.

"""
Database interface for platform table.
"""

__revision__ = '$Rev: 259 $'
__date__ = '$Date: 2006-05-31 17:28:15 +0200 (Wed, 31 May 2006) $'
__author__ = '$Author: johann $'

def get_name_dict():
    """
    Get a mapping from lowercase platform name to id (numeric primary key).
    """
    cur.execute('SELECT platform, name FROM platform')
    result = {}
    for platform, name in cur.fetchall():
        if name == 'Mac OS':
            name = 'Mac'
        result[name.lower()] = platform
    return result
