# $URL: https://pyisapie.svn.sourceforge.net/svnroot/pyisapie/Tags/1.1.0-rc4/PyISAPIe/Python/Examples/Advanced/Watch.py $
# $Rev: 91 $ $Date: 2008-01-10 23:53:59 -0800 (Thu, 10 Jan 2008) $
# (C)2008 Phillip Sitbon <phillip@sitbon.net>
#
"""File change notification.

This module allows you to monitor a module for changes
and reload it when necessary. This implementation isn't
exactly the most efficient; it would save a few threads
if a list of watched *folders* were kept so that a list
of callbacks associated with modules in those folders
could be called from a single thread monitoring it.
"""
__all__ = ('Watch',)

import win32event, win32file, win32con, os, sys
from threading import Thread

WatchList = []

# Sometimes the notification will not go through due to a
# problem with networked folders. I've had some luck getting
# this to work a little better when the timeout is 1 second
# (Timeout = 1) because the stat() call sees the change.
# I did notice a slight decrease in performance when using
# non-infinite timeouts.
#
# Also, sometimes the text editor seems to make a difference;
# using the IDLE editor most changes are not recognized, but
# the Visual Studio IDE and Notepad2 are almost always
# guaranteed to cause a reload.
#
Timeout = win32event.INFINITE

def Watch( Module, Callback, * Args, ** Kwds ):
  if Module.__file__ in WatchList:
    return

  T = Thread(target = WatchThread, args=(Module,Callback,Args,Kwds))
  T.setDaemon(True)
  T.start()

def WatchThread( Module, Callback, Args, Kwds ):
  global WatchList
  File = Module.__file__

  if File.endswith('.pyc') or File.endswith('.pyo'):
    File = File[:-1]

  if File in WatchList:
    # Already monitoring for this file
    return

  WatchList.append(File)

  try:
    Handle = win32file.FindFirstChangeNotification(os.path.dirname(File),False,
      win32con.FILE_NOTIFY_CHANGE_LAST_WRITE)

    Last = os.stat(File)

    while 1:
      if win32event.WaitForSingleObject(Handle, Timeout) == win32event.WAIT_OBJECT_0:
        win32file.FindNextChangeNotification(Handle)

      Cur = os.stat(File)

      # If _anything_ has changed, call the callback. This includes things
      # other than modify time.
      if Cur != Last:     
        Callback(Module, *Args, **Kwds)

      Last = Cur

  except:
    # doesn't do anything with exceptions and makes sure cleanup
    # goes smoothly
    #

    try:
      WatchList.remove(File)
      win32file.FindCloseChangeNotification(Handle)
    except:
      pass
