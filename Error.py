# $URL: https://pyisapie.svn.sourceforge.net/svnroot/pyisapie/Tags/1.1.0-rc4/PyISAPIe/Python/Examples/Advanced/WWW/Error.py $
# $Rev: 91 $ $Date: 2008-01-10 23:53:59 -0800 (Thu, 10 Jan 2008) $
# (C)2008 Phillip Sitbon <phillip@sitbon.net>
#
"""Default error handler.
"""
from Http import *

def HandleNotFound(URL):
  Txt = """
    <html><body>
    <h1>Error 404</h1>
    <br>
    The url '%s' was not found.
    </body></html>

  """ % URL

  Header( "Content-type: text/html",
    Length = len(Txt),
    Status = 404,
    Close = True
  )

  Write(Txt)