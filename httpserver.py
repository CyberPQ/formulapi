"""Simple HTTP Server.

This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.
http://www.acmesystems.it/python_httpd

"""

import os
import posixpath
import BaseHTTPServer
import urllib
import urlparse
import cgi
import sys
import shutil
import mimetypes
from PIL import Image
import datetime

import imagebuffer

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    """Simple HTTP request handler with GET and HEAD commands.
    """

    server_version = "SimpleHTTP/version"

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        if path == '/capture.png':
            if imagebuffer.width > 0:
                print datetime.datetime.now(),'start capture'
                # Send the html message
                img = Image.fromstring(imagebuffer.mode, (imagebuffer.width,imagebuffer.height), imagebuffer.data)
                pseudofile = StringIO()
                print datetime.datetime.now(),'start png'
                img.save(pseudofile,'PNG')
                pseudofile.seek(0, os.SEEK_END)
                size = pseudofile.tell()
                print datetime.datetime.now(),'fin capture'
                #send response and data
                self.send_response(200)
                self.send_header('Content-Type', 'image/png')
                self.send_header('Content-Length', size)
                self.end_headers()
                self.wfile.write(pseudofile.getvalue())
                pseudofile.close()
                print datetime.datetime.now(),'fin response'
        else:
            self.send_error(404, "File not found")



    def translate_path(self, path):
        """Translate a /-separated PATH
        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        
        return path

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """

        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })


def test(HandlerClass = RequestHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    test()
