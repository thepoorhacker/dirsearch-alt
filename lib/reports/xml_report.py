# -*- coding: utf-8 -*-
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Author: Mauro Soria

from lib.reports import *
import time


class XMLReport(FileBaseReport):
    def addPath(self, path, status, response):
        contentLength = None

        try:
            contentLength = int(response.headers["content-length"])

        except (KeyError, ValueError):
            contentLength = len(response.body)

        self.storeData((path, status, contentLength, response.redirect))

    def generate(self):
        result = "<?xml version=\"1.0\"?>\n"

        headerName = "{0}://{1}:{2}/{3}".format(
            self.protocol, self.host, self.port, self.basePath
        )

        result += "<time>{0}</time>\n".format(time.ctime())
        result += "<target url=\"{0}\">\n".format(headerName)

        for path, status, contentLength, redirect in self.pathList:
            result += " <info path=\"/{0}\">\n".format(path)
            result += "  <status>{0}</status>\n".format(status)
            result += "  <contentLength>{0}</contentLength>\n".format(contentLength)
            result += "  <redirect>{0}</redirect>\n".format(redirect)
            result += " </info>\n"

        result += "</target>\n"

        return result
