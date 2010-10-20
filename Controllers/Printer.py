"""Print service handler script.
"""

import logging

from os.path import basename, getsize
from os import unlink, listdir, sep, stat
import time
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile, gettempdir
import re
import urlparse

"""
This special imports are needed to support Python 2.5
"""
try: import json
except ImportError: import simplejson as json
try: from urlparse import parse_qs
except ImportError: from cgi import parse_qs



from Http import *

#TODO: Get this from config
JAR_PATH = "C:\\Python25\\MapFish\\print-standalone-1.2-SNAPSHOT.jar"
CONFIG_PATH = "C:\\Python25\\MapFish\\test.yaml"

"""
Logging setup
http://docs.python.org/library/logging.html#configuring-logging-for-a-library
"""
log = logging.getLogger(__name__)
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
h = NullHandler()
log.addHandler(h)


class PrintController:
    """ Map printing service based on the MapFish print module """
    
    TEMP_FILE_PREFIX = "mfPrintTempFile"
    TEMP_FILE_SUFFIX = ".pdf"
    TEMP_FILE_PURGE_SECONDS = 600
    
    """
    See _urlForAction for details
    """   
    actionsMap = {
        "info":"info.json",
        "doPrint":"print.pdf",
        "create":"create.pdf",
        "get":"%id%.pdf"
        }
    
    def __init__(self):
        self._setupConfig()
    
    def info(self):
        """
        To get (in JSON) the information about the available formats and CO.
        """
        cmd = ['java', '-cp', self.jarPath, 'org.mapfish.print.ShellMapPrinter',
               '--config=' + self.configPath, '--clientConfig', '--verbose='+_getJavaLogLevel()]
        self._addCommonJavaParams(cmd)
        
        exe = Popen(cmd, stdout = PIPE, stderr = PIPE)
        result = exe.stdout.read()
        error = exe.stderr.read()
        if len(error)>0:
           log.error(error)
        ret = exe.wait()
        Header("Content-Type: text/plain")
        if ret == 0:
            result = self._addURLs(result)
            callback = self._getQueryStringParam("var")
            if callback:
                Header( "Content-type: text/javascript; charset=utf-8", Status = 200)
                Write("var " + callback + "=" + result + ";")
            else:
                Header( "Content-type: application/json; charset=utf-8", Status = 200)
                Write(result)          
        else:
            Header( "Content-type: text/plain; charset=utf-8", Status = 500)
            Write("ERROR(" + str(ret) + ")\n\n" + error)
      
    def doPrint(self):
        Header("Content-Type: text/plain")
        Write("print.pdf request received ")
      
    def create(self):
        Header("Content-Type: text/plain")
        Write("create.json request received ")
      
    def get(self,id):
        Header("Content-Type: text/plain")
        Write("<id>.pdf request received with id = " + str(id))

    def _addCommonJavaParams(self, cmd):
        """
        Adds the java system properties for the locale. Gets it from the request
        parameter "locale" or try to guess it from the "Accept-Language" HTTP
        header parameter.
        Adds as well the referer.
        """

        referer = getattr(Env,"HTTP_REFERER", False)
        if referer:
            cmd.append("--referer="+referer)

        #allows to run the process without X11
        cmd.insert(1, "-Djava.awt.headless=true")
        
        locale = getattr(Env,"HEADER_LOCALE", False)
        
        if not locale:
            accept_language = getattr(Env,"HEADER_ACCEPT-LANGUAGE", False)
            if accept_language:
                locale = accept_language.split(',')[0]
            else:
                return
        splitted = re.split("[-_]", locale)
        language = splitted[0]
        cmd.insert(1, "-Duser.language="+language)
        if len(splitted)>1:
            country = splitted[1]
            cmd.insert(1, "-Duser.country="+country)      
      
    def _setupConfig(self):
        #TODO: Get this from config
        self.jarPath = JAR_PATH
        self.configPath = CONFIG_PATH      

    def _urlForAction(self, actionName, id = None):
        """
        MapFish uses the Pylons functions to get info about the actions URLs
        from the controller. As this is not possible in PyISAPIe, we need to
        manually define the mapping in self.actionsMap
        """
        if actionName in self.actionsMap:
            endPoint = self.actionsMap[actionName]
            if actionName == "get":
                endPoint = endPoint.replace("%id%",id)
        else:
            return False
         
        url = getattr(Env,"URL")
        path = url[0:url.rfind("/")]
        baseurl = self._getQueryStringParam("baseurl")
        if baseurl:
            return baseurl + endPoint
        
        protocol = getattr(Env,"SERVER_PROTOCOL").split('/')[0].lower()
        host = getattr(Env,"SERVER_NAME")
        return urlparse.urlunparse((protocol, host, path + "/" + endPoint, None, None, None))        
        
    def _addURLs(self, result):
        expr = re.compile('}$')
        printURL = json.dumps(self._urlForAction("doPrint"))
        createURL = json.dumps(self._urlForAction("create"))
        return expr.sub(',"printURL":' + printURL + ',' +
                        '"createURL":' + createURL + '}', result)
    
    def _getQueryStringParam(self,name,default = False):
        qs = getattr(Env,"QUERY_STRING",False)
        if qs:
            qs = parse_qs(qs)
            if name in qs:
                return qs[name][0]
        return default
        
        
def _getJavaLogLevel():
    """
    Convert the python log level into a value to be used with the java
    "--verbose" parameter
    """
    level = log.getEffectiveLevel()
    if level >= 30:
        return '0'
    elif level >= 20:
        return '1'
    else:
        return '2' 

        
"""
This are the handlers mapped by PyISAPie
"""
printer = PrintController()
def info():
    printer.info()
  
def doPrint():
    printer.doPrint()
  
def create():
    printer.create()
  
def get(id):
    printer.get(id)
