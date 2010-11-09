"""Default page handler.
"""
from PyISAPIe import Env
from hashlib import md5
import imp

from Error import HandleNotFound

Handlers = {}


def Request(Path):
  Script = Env.SCRIPT_NAME
  Key = Name = '__'+md5(Script).hexdigest().upper()
  Handler = Handlers.get(Key, None)

  if not Handler:
    try:
      Handlers[Key] = imp.load_source(Key, Env.SCRIPT_TRANSLATED).Request
    except Exception, Val:
      # trigger a passthrough to the next ISAPI handler -
      # ONLY WORKS FOR WILDCARD APPLICATION MAPPINGS
      #return True
      # or just fail, preferable for an application map
      if type(Val).__name__ == "IOError":
        HandleNotFound(Path)
      else:
        raise ImportError, "[Loading '%s'] %s" % (Env.SCRIPT_TRANSLATED, str(Val))


  return Handlers[Key]()