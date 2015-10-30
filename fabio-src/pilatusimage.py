# coding: utf-8
#
#    Project: X-ray image reader
#             https://github.com/kif/fabio
#
#
#    Copyright (C) European Synchrotron Radiation Facility, Grenoble, France
#
#    Principal author:       Jérôme Kieffer (Jerome.Kieffer@ESRF.eu)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""

Authors:
........
* Henning O. Sorensen & Erik Knudsen:
  Center for Fundamental Research: Metal Structures in Four Dimensions;
  Risoe National Laboratory;
  Frederiksborgvej 399;
  DK-4000 Roskilde;
  email:erik.knudsen@risoe.dk
* Jon Wright:
  European Synchrotron Radiation Facility;
  Grenoble (France)

"""
# Get ready for python3:
from __future__ import with_statement, print_function


# Base this on the tifimage (as Pilatus is tiff with a
# tiff header

from .tifimage import TifImage


class PilatusImage(TifImage):
    """ Read in Pilatus format, also
        pilatus images, including header info """


    def _readheader(self, infile):
        """
        Parser based approach
        Gets all entries
        """

        self.header = {}

#        infile = open(infile)
        hstr = infile.read(4096)
        # well not very pretty - but seems to find start of
        # header information
        if (hstr.find('# ') == -1):
            return self.header

        hstr = hstr[hstr.index('# '):]
        hstr = hstr[:hstr.index('\x00')]
        hstr = hstr.split('#')
        go_on = True
        while go_on:
            try:
                hstr.remove('')
            except Exception:
                go_on = False

        for line in hstr:
            line = line[1:line.index('\r\n')]
            if line.find(':') > -1:
                dump = line.split(':')
                self.header[dump[0]] = dump[1]
            elif line.find('=') > -1:
                dump = line.split('=')
                self.header[dump[0]] = dump[1]
            elif line.find(' ') > -1:
                i = line.find(' ')
                self.header[line[:i]] = line[i:]
            elif line.find(',') > -1:
                dump = line.split(',')
                self.header[dump[0]] = dump[1]

        return self.header



    def _read(self, fname):
        """
        inherited from tifimage
        ... a Pilatus image *is a* tif image
        just with a header
        """
        return tifimage.read(self, fname)

pilatusimage = PilatusImage
