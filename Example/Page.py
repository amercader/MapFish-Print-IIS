# $URL: https://pyisapie.svn.sourceforge.net/svnroot/pyisapie/Tags/1.1.0-rc4/PyISAPIe/Python/Examples/Advanced/WWW/Example/Page.py $
# $Rev: 91 $ $Date: 2008-01-10 23:53:59 -0800 (Thu, 10 Jan 2008) $
# (C)2008 Phillip Sitbon <phillip@sitbon.net>
#
"""Example handler script.
"""

from Http import *

def PlainText(Path):
  Header("Content-Type: text/plain")
  Write("This is a plain-text page.\r\nExtra path info: " + str(Path))

def Html(Path):
  Header("Content-Type: text/html")
  Write("<h2>This is an html page.</h2><br>\r\n<em>Extra path info: " + str(Path) + "</em>")
