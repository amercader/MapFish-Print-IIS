# $URL: https://pyisapie.svn.sourceforge.net/svnroot/pyisapie/Tags/1.1.0-rc4/PyISAPIe/Python/Examples/Advanced/WWW/Example/__init__.py $
# $Rev: 91 $ $Date: 2008-01-10 23:53:59 -0800 (Thu, 10 Jan 2008) $
# (C)2008 Phillip Sitbon <phillip@sitbon.net>
#
"""Example package.

The handler below corresponds to /dev/example/
(_not_ /dev/example !)
"""
from Http import *

def Index():
  Txt = """
    <html><body>
    <h1>Example Index</h1>
    <ul>
      <li><a href="plain-text">Plain text page</a></li>
      <li><a href="html">HTML page</a></li>
    </ul>
    </html></body>
  """
  
  Header("Content-Type: text/html", Length = len(Txt))
  Write(Txt)
