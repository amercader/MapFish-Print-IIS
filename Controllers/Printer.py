"""Print service handler script.
"""

import logging

from os.path import basename, getsize, exists
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
TEMP_DIR = "C:\\Python25\\PyISAPIe\\tmp"


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
        """
        All in one method: creates and returns the PDF to the client.
        """
        cmd = ['java', '-cp', self.jarPath, 'org.mapfish.print.ShellMapPrinter',
             '--config=' + self.configPath, '--verbose='+_getJavaLogLevel()]
        self._addCommonJavaParams(cmd)
        spec = self._getQueryStringParam("spec")
        exe = Popen(cmd, stdin = PIPE, stdout = PIPE, stderr = PIPE)
        exe.stdin.write(spec)
        exe.stdin.close()
        result = exe.stdout.read()
        error = exe.stderr.read()
        if len(error)>0:
            log.error(error)
        ret = exe.wait()
        if ret == 0:
            Header( "Content-type: application/pdf", Status = 200)
            Write(result)            
        else:
            Header( "Content-type: text/plain; charset=utf-8", Status = 500)
            Write("ERROR(" + str(ret) + ")\n\n" + error)
      
    def create(self):
        """
        Create the PDF and returns to the client (in JSON) the URL to get the
        PDF.
        """
        self._purgeOldFiles()
        #TODO: access denied in C: windows temp
        #pdfFile = NamedTemporaryFile("w+b", -1, self.TEMP_FILE_SUFFIX, self.TEMP_FILE_PREFIX)
        pdfFile = NamedTemporaryFile("w+b", -1, self.TEMP_FILE_SUFFIX, self.TEMP_FILE_PREFIX,TEMP_DIR)
        pdfFilename = pdfFile.name
        pdfFile.close()
        cmd = ['java',
               '-cp', self.jarPath,
               'org.mapfish.print.ShellMapPrinter',
               '--config=' + self.configPath,
               '--verbose='+_getJavaLogLevel(),
               '--output=' + pdfFilename]
        self._addCommonJavaParams(cmd)
        spec = self._getQueryStringParam("spec")
        exe = Popen(cmd, stdin = PIPE, stderr = PIPE)
        exe.stdin.write(spec)
        exe.stdin.close()
        error = exe.stderr.read()
        if len(error)>0:
            log.error(error)
        ret = exe.wait()
        if ret == 0:
            curId = basename(pdfFilename)[len(self.TEMP_FILE_PREFIX):-len(self.TEMP_FILE_SUFFIX)]
            getURL = self._urlForAction("get", id = curId)
            
            Header( "Content-type: application/json; charset=utf-8", Status = 200)
            Write(
                json.dumps({
                    'getURL': getURL,
                    'messages': error
                })
            )
        else:
            try:
                unlink(pdfFilename)
            except OSError:
                pass
            Header( "Content-type: text/plain; charset=utf-8", Status = 500)
            Write("ERROR(" + str(ret) + ")\n\nspec=" + spec + "\n\n" + error)

    def get(self,id):
        """
        To get the PDF created previously.
        """
        #TODO: access denied in C: windows temp
        #name = gettempdir() + sep + self.TEMP_FILE_PREFIX + id + self.TEMP_FILE_SUFFIX
        name = TEMP_DIR + sep + self.TEMP_FILE_PREFIX + id + self.TEMP_FILE_SUFFIX
        """
        MapFish uses the FileApp method from Paste that handles all the things related 
        with serving files. We will only handle 404 and 403 errors.
        """
        if not exists(name):
            Header( "Content-type: text/plain; charset=utf-8", Status = 404 )
            Write("Not found")
        else:

            try:
                file = open(name, 'rb')
            except (IOError, OSError), e:
                Header( "Content-type: text/plain; charset=utf-8", Status = 403 )
                Write("You are not allowed to access this file (%s)" % e)
            contents = file.read()
            file.close()
            
            Header(
                [
                    
                    "Content-Type: application/pdf",
                    "Content-Disposition: attachment; filename="+id+".pdf",
                    "Pragma: public",
                    "Expires: 0",
                    "Cache-Control: private"
                ],
                Status = 200,
                Length = getsize(name)
            )
            Write(contents)
            
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
    
    def _purgeOldFiles(self):
        """
        Delete temp files that are more than TEMP_FILE_PURGE_SECONDS seconds old
        """
        #TODO: access denied in C: windows temp
        #files=listdir(gettempdir())
        files=listdir(TEMP_DIR)
        for file in files:
            if file.startswith(self.TEMP_FILE_PREFIX) and file.endswith(self.TEMP_FILE_SUFFIX):
                #TODO: access denied in C: windows temp
                #fullname = gettempdir() + sep + file
                fullname = TEMP_DIR + sep + file
                age = time.time() - stat(fullname).st_mtime
                if age > self.TEMP_FILE_PURGE_SECONDS:
                    log.info("deleting leftover file :" + fullname + " (age=" + str(age) + "s)")
                    unlink(fullname)
                    
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
