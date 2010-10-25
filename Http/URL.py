# $URL: https://pyisapie.svn.sourceforge.net/svnroot/pyisapie/Tags/1.1.0-rc4/PyISAPIe/Python/Examples/Advanced/URL.py $
# $Rev: 91 $ $Date: 2008-01-10 23:53:59 -0800 (Thu, 10 Jan 2008) $
# (C)2008 Phillip Sitbon <phillip@sitbon.net>
#
"""URL mapping module.

This module allows you to specify a variable (Map) in
the WWW.URL module that will use regular expressions
to match URLs to modules. All the modules are preloaded
and the regular expressions are pre-compiled.

The format of the URL map entries can be recursive.
A key either specifies a module/package, in which case
the value is a dictionary where keys are either the same
(module name key, dictionary as value), or just regex
to function name mappings (strings for key and value).

See the example setup in the WWW folder - it will make
more sense than the description above.

You might want to change either the code here or in
Isapi.py to handle the NotFoundError exception if you
don't plan on having a default map (empty regex).
"""
__all__ = ( \
  'NotFoundError',
  'HandleRequest',
 )

from Http import Config, Env
#adria
#from Http.Watch import Watch
from WWW.URL import Map
from sys import modules
from re import search
import re, sys

class NotFoundError(Exception):
  pass

Prefix = 'WWW.'
FromList = ('WWW',)

FastMaps = []
Cache = {}

def LoadMaps(Maps, Prefix = Prefix):

  if isinstance(Maps, list):
    for Item in Maps:
      # TODO: Check that items are dicts?
      LoadMaps(Item, Prefix)
      
    return

  for Key, Value in Maps.items():

    if isinstance(Value, dict):
      LoadMaps(Value, Prefix + Key + '.')

    else:
      Value = Prefix + Value
      Mod, Handler = Value.rsplit('.', 1)
      AddMap(Key, Mod, Handler)


def AddMap( Pattern, Module, Handler ):
    Search = re.compile(Pattern).search
	
    #adria
    #if Config.Debug:
        #Module, Handler = InstallDebugHandler(Module, Handler)
    #else:
    Module = __import__(Module,globals(),locals(),FromList)
    Handler = getattr(Module,Handler)

    FastMaps.append( (Search, Handler, Module) )


def Reloader( Mod, HandlerName ):
  global FastMaps
  global Cache

  I = 0
  for Search, Handler, M in FastMaps:
    if Handler.__name__ == HandlerName and M == Mod:
      NewHandler = getattr(reload(Mod), HandlerName)
      L = list(FastMaps)
      L[I] = (Search, NewHandler, M)
      FastMaps = tuple(FastMaps)

      
      for URL, (Hndlr, Args, M) in Cache.items():
        if M == Mod and Hndlr.__name__ == NewHandler.__name__:
          Cache[URL] = (NewHandler, Args, M)

      break

    I += 1


def InstallDebugHandler( Module, Handler ):
  Module = __import__(Module,globals(),locals(),FromList)
  HandlerFn = getattr(Module,Handler)

  Watch(Module, Reloader, Handler)

  return Module, HandlerFn


def HandleRequest():
  URL = Env.URL

  I = Cache.get(URL)
  
  if I:
    return I[0](* I[1])

  for Search, Handler, Mod in FastMaps:
    Match = Search(URL)
    if not Match:
      continue

    Cache[URL] = (Handler, Match.groups(), Mod)
    return Handler(*Match.groups())


  raise NotFoundError, URL

# Call the load function
# TODO: see if this causes debug issues. maybe always
#  load based on config?

if not FastMaps:
  LoadMaps(Map)
  FastMaps = tuple(FastMaps)
