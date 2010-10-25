# $URL: https://pyisapie.svn.sourceforge.net/svnroot/pyisapie/Tags/1.1.0-rc4/PyISAPIe/Python/Examples/Advanced/Isapi.py $
# $Rev: 91 $ $Date: 2008-01-10 23:53:59 -0800 (Thu, 10 Jan 2008) $
# (C)2008 Phillip Sitbon <phillip@sitbon.net>
#
"""Global ISAPI request handler.

This version just proxies the request handler to
the URL mapping handler.
"""
from Http import URL

Request = URL.HandleRequest