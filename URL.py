# $URL: https://pyisapie.svn.sourceforge.net/svnroot/pyisapie/Tags/1.1.0-rc4/PyISAPIe/Python/Examples/Advanced/WWW/URL.py $
# $Rev: 91 $ $Date: 2008-01-10 23:53:59 -0800 (Thu, 10 Jan 2008) $
# (C)2008 Phillip Sitbon <phillip@sitbon.net>
#
"""URL map example module.

All entries must be dictionaries- the map structure
has been changed to a list to impose order.

The maps are recursive, meaning that if a value
is a dictionary, then all names in it are prefixed
with the key of that entry.
"""

Map = [

  {
    'Example' :
    {
      '^/printing/example/$' : 'Index',

      'Page' :
      {
        '^/printing/example/plain-text(?:(/[a-zA-Z0-9-/]+))?$' : 'PlainText',
        '^/printing/example/html(?:(/[a-zA-Z0-9-/]+))?$'       : 'Html',
      },
    },
    'Controllers' :
    {
        'Printer' :
        {
                   
            '^/printing/info.json' : 'info',
            '^/printing/print.pdf?$' : 'doPrint',
            '^/printing/create.json' : 'create',
            '^/printing/(?:([a-zA-Z0-9]+)).pdf$' : 'get',
            
        }
    }
  },

  {'(.*)' : 'Error.HandleNotFound'},

  # Same as the above line:
  #
  #{
  #  'Error' :
  #  {
  #    '(.*)' : 'HandleNotFound',
  #  },
  #}
]