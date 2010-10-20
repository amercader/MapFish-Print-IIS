"""Print service handler script.
"""

#import json
import logging

from os.path import basename, getsize
from os import unlink, listdir, sep, stat
import time
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile, gettempdir
import re

try: import json
except ImportError: import simplejson as json

try: from urlparse import parse_qs
except ImportError: from cgi import parse_qs

import urlparse

from Http import *

#TODO: Get this from config

class PrintController:
    TEMP_FILE_PREFIX = "mfPrintTempFile"
    TEMP_FILE_SUFFIX = ".pdf"
    TEMP_FILE_PURGE_SECONDS = 600
    
    def info(self):
        Header("Content-Type: text/plain")
        Write("info.json request received")
      
    def doPrint(self):
        qs = parse_qs(getattr(Env,"QUERY_STRING"))
        Header("Content-Type: text/plain")
        Write(qs["spec"][0])

    
        #Header("Content-Type: text/plain")
        #Write("print.pdf request received ")
      
    def create(self):
      Header("Content-Type: text/plain")
      Write("create.json request received ")
      
    def get(self,id):
      Header("Content-Type: text/plain")
      Write("<id>.pdf request received with id = " + str(id))
 

printer = PrintController()
def info():
    printer.info()
  
def doPrint():
    printer.doPrint()
  
def create():
    printer.create()
  
def get(id):
    printer.get(id)
