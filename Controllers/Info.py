# $URL: https://pyisapie.svn.sourceforge.net/svnroot/pyisapie/Tags/1.1.0-rc4/PyISAPIe/Python/Examples/Info.py $
# $Rev: 153 $ $Date: 2009-05-23 19:31:38 -0700 (Sat, 23 May 2009) $
# (C)2008 Phillip Sitbon <phillip@sitbon.net>
#
"""Some information on the request and environment.

Call Request() to write out the formatted info.
"""
from Http import Version
from Http import *
import sys, os, thread

OtherDataVars = \
  [
    "Version",
    "Version.Full",
    "sys.version",
    "__interp__",
    "sys.executable",
    "sys.prefix",
    "sys.exec_prefix",
    "sys.path",
    "os.getpid()",
    "thread.get_ident()",
  ]

Body = """
<html>
<head>
  <title>PyISAPIe Information Page</title>
</head>
<body style="font-family: Verdana; font-size: 8pt; margin: 5px; padding: 0px;">

<p style="font-family: Verdana; font-size: 18pt; width: 100%%; margin:0px; text-align: center; background: #77809A; border: black 1px solid; color: black;">
PyISAPIe Information Page
<div style="background: #DDDDFF; border: black 1px solid;border-top: none; width:100%%;">
<br>
<p style="margin: 5px;">%s<br><br></p>
</div>
</div>
</p>
</body>
</html>
"""

def Request():
  Content = ""
  Content += GetOtherData()
  Content += GenerateEnvTable()
  Content += GetHeaders()
  Content += GetPostData()
  Content = Body % Content
  Header("Content-Type: text/html", Length = len(Content))
  Write(Content)

Table = """
<table width=95%% cellspacing=1 cellpadding=3 align=center style="font-size:8pt; background: #9999AA;">
  <tr>
    <td colspan=2 align=center style="background: #AAAABB; font-weight: bold; font-size: 14pt;">
      %s
    </td>
  </tr>
  <tr>
    <td align=center width="30%%" style="font-weight: bold; background: #CCCCDD; font-size:10pt;">
      Variable Name
    </td>
    <td align=center style="font-weight: bold; background: #CCCCDD; font-size:10pt;">
      Value
    </td>
  </tr>
  %s
</table><br><br>
"""

EnvVars = ( \
  #'ALL_RAW',
  'APP_POOL_ID',
  'APPL_MD_PATH',
  'APPL_PHYSICAL_PATH',
  'AUTH_PASSWORD',
  'AUTH_TYPE',
  'AUTH_USER',
  'CACHE_URL',
  'CERT_COOKIE',
  'CERT_FLAGS',
  'CERT_ISSUER',
  'CERT_KEYSIZE',
  'CERT_SECRETKEYSIZE',
  'CERT_SERIALNUMBER',
  'CERT_SERVER_ISSUER',
  'CERT_SERVER_SUBJECT',
  'CERT_SUBJECT',
  'CONTENT_LENGTH',
  'CONTENT_TYPE',
  'GATEWAY_INTERFACE',
  #'HTTP_ACCEPT',
  'HTTP_ACCEPT_ENCODING',
  'HTTP_ACCEPT_LANGUAGE',
  'HTTP_CONNECTION',
  'HTTP_COOKIE',
  'HTTP_HOST',
  'HTTP_REFERER',
  'HTTP_URL',
  'HTTP_USER_AGENT',
  'HTTP_VERSION',
  'HTTPS',
  'HTTPS_KEYSIZE',
  'HTTPS_SECRETKEYSIZE',
  'HTTPS_SERVER_ISSUER',
  'HTTPS_SERVER_SUBJECT',
  'INSTANCE_ID',
  'INSTANCE_META_PATH',
  'LOCAL_ADDR',
  'LOGON_USER',
  'PATH_INFO',
  'PATH_TRANSLATED',
  'QUERY_STRING',
  'REMOTE_ADDR',
  'REMOTE_HOST',
  'REMOTE_PORT',
  'REMOTE_USER',
  'REQUEST_METHOD',
  'SCRIPT_NAME',
  'SCRIPT_TRANSLATED',
  'SERVER_NAME',
  'SERVER_PORT',
  'SERVER_PORT_SECURE',
  'SERVER_PROTOCOL',
  'SERVER_SOFTWARE',
  'SSI_EXEC_DISABLED',
  'UNENCODED_URL',
  'UNMAPPED_REMOTE_USER',
  'URL',
 )

def GenerateEnvTable():
  Td = """<tr><td align=left style="background: #CCCCDD; font-size:8pt;">%s"""+\
       """</td><td align=left style="font-family: Courier New; background: #CCCCDD; font-size:8pt;">"""+\
       "%s</td><tr>\n"

  Result = ''
  for Var in EnvVars:
    Result += Td % (Var, getattr(Env, Var))
  return Table % ("Environment Variables", Result)

HeaderBox = """
<table width=95%% cellspacing=1 cellpadding=3 align=center style="font-size:8pt; background: #9999AA;">
  <tr>
    <td align=center style="background: #AAAABB; font-weight: bold; font-size: 14pt;">
      Client Headers
    </td>
  </tr>
  <tr>
    <td align=left style="font-family: Courier New; background: #CCCCDD; font-size:8pt;">
      <pre>%s</pre>
    </td>
  </tr>
</table><br><br>
"""

def GetHeaders():
  return HeaderBox % Env.ALL_RAW


PostBox = """
<table width=95%% cellspacing=1 cellpadding=3 align=center style="font-size:8pt; background: #9999AA;">
  <tr>
    <td align=center style="background: #AAAABB; font-weight: bold; font-size: 14pt;">
      POST Data
    </td>
  </tr>
  <tr>
    <td align=left style="font-family: Courier New; background: #CCCCDD; font-size:8pt;">
      <pre>%s</pre>
    </td>
  </tr>
</table><br><br>
"""

def GetPostData():
  Data = Read()
  if not Data:
    Data = "\r\n\r\n"
  return PostBox % Data

def GetOtherData():
  Td = """<tr><td align=left style="background: #CCCCDD; font-size:8pt;">%s"""+\
       """</td><td align=left style="font-family: Courier New; background: #CCCCDD; font-size:8pt;">"""+\
       "%s</td><tr>\n"

  Result = ''
  for Var in OtherDataVars:
    Val = eval(Var)
    if isinstance(Val, (list, tuple)):
      Val = "<br>".join(str(X) for X in Val)
    elif isinstance(Val, dict):
      Val = "<br>".join("%s: %s" % (str(K), str(V)) for K, V in Val.items())

    Result += Td % (Var, Val)
  return Table % ("Misc. Data", Result)
