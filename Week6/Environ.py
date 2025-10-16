#!/usr/bin/env python
'''
# Content of 'Environ.py'

# This file is to be open and read and executed in the "current Python session" by using :
# 
#   with open( 'Environ.py' ) as file123 :      # any legal file path of this file will do
#     exec( file123.read() )
#
# This is so that the functions contained in this file are able to share globals()
# with the current Python session. Only when sharing the same globals() can the actions
# performed by Export(), DeExport(), SyncCV(), (revised) B(), B1() make sense.
#
# Note : Must have already run 'from StartUpScript import *' (or similar) before running this script.
#
# # Next two lines are temporarily commented, because 'from StartUpScript import *' is commented
# # Warning : It is strongly advised to read-and-exec this file AT THE START OF the Python session,
# #           because it contains 'from StartUpScript import *' which will cause overrides.
#
# Usage :
# 
#   Export( 'abc' )      : export the global var. named 'abc' as an environment variable.
#   DeExport( 'abc' )    : make the (supposed) global var. named 'abc'a non-env.-var.
#   ChangeCWD( path )    : Change the current working directory according 
#                          (no tilde substitution or path name expansion)
#   PrintCWD()           : What is the current working directory?
#   IsEnv( 'abc' )       : checking whether the (supposed) global var. named 'abc' is an env. var.
#   PrintEnv( 'abc' )    : Get the value of the env. var. named 'abc'
#   PrintAllEV()         : Print the list of all env. var.
#   PrintAllEV1()        : Print the list of all env. var. (with values also printed)
#   B( cmd )             : Use bash to execute the given cmd and print its output.
#                          cmd should not contain >>'<<.
#   B1( cmd )            : Use bash to execute the given cmd and return two strings :
#                          (1) output (to stdin) of the being executed cmd, (2) the final exit status.
#                          cmd should not contain >>'<<.
#
# Caution :
#
#   1. 'from StartUpScript import *' must be executed in the CURRENT Python session BEFORE 
#      opening and reading (the content of) and executing (the content of) this file.
#
#   2. DO NOT change >>__os_environ_original__<<
#
#   3. Values of globals and their counterparts in os.environ are not automatically synchronized.
#
# Usage :

Ubuntu > ls
... Environ.py ...
Ubuntu > cp Environ.py ~/bin/Environ.py
Ubuntu > python -i ~/bin/StartUpScript.py
>>> with open( 'Environ.py' ) as file123 :
...   exec( file123.read() )
... 
>>> aaa = 10
>>> Export( 'aaa' )
>>> bbb = 20
>>> Export( 'bbb' )
>>> B( 'PrintPara aaa=$aaa bbb=$bbb "Hi OK"' )
Num of Para. : 4
Para. $0 : PrintPara
Para. $1 : aaa=10
Para. $2 : bbb=20
Para. $3 : Hi OK
>>> DeExport( 'bbb' )
>>> B( 'PrintPara aaa=$aaa bbb=$bbb "Hi OK"' )
Num of Para. : 4
Para. $0 : PrintPara
Para. $1 : aaa=10
Para. $2 : bbb=
Para. $3 : Hi OK
>>> B( 'PrintPara aaa=$aaa bbb=$bbb "Hi OK" > file1' )
>>> B( 'ls' )
Environ.py
...
file1
...
>>> B( 'PrintPara `date`' )
Num of Para. : 7
Para. $0 : PrintPara
Para. $1 : Sat
Para. $2 : Oct
Para. $3 : 12
Para. $4 : 00:44:37
Para. $5 : CST
Para. $6 : 2024
>>> B( 'PrintPara "`date`"' )
Num of Para. : 2
Para. $0 : PrintPara
Para. $1 : Sat Oct 12 15:54:19 CST 2024
>>> dir()
['B', 'DeExport', 'Export', 'IsEnv', 'PrintEV', 'PrintEV1', 'S', 'SyncEV', 'U', 'U1', '__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__os_environ_original__', '__package__', '__spec__', '__warningregistry__', 'aaa', 'bbb', 'ccc', 'echo', 'file123', 'os', 'pp', 'pprint', 'subprocess', 'sys']

>>> help( Export )
Help on function Export in module __main__:

Export(aVarName)
    Export( 'abc' ) : export the global var. named 'abc' as an environment variable.
(END)
>>> 
>>> aaa = 10
>>> hi = 'whatever will be will be'
>>> bbb = 20
>>> Export( 'aaa' )
>>> Export( 'bbb' )
>>> a,b = B1( 'PrintPara aaa=$aaa hi=$hi bbb=$bbb ~ "Hi there"' )
>>> print(a) ; print(b)
Number of parameters : 6
Para 0 >>PrintPara<<
Para 1 >>aaa=10<<
Para 2 >>hi=<<
Para 3 >>bbb=20<<
Para 4 >>/home/hsia<<
Para 5 >>Hi there<<
0
>>> DeExport( 'bbb' )
>>> a,b = B1( 'PrintPara aaa=$aaa hi=$hi bbb=$bbb ~ "Hi there"' )
>>> print(a) ; print(b)
Number of parameters : 6
Para 0 >>PrintPara<<
Para 1 >>aaa=10<<
Para 2 >>hi=<<
Para 3 >>bbb=<<
Para 4 >>/home/hsia<<
Para 5 >>Hi there<<
0
>>> aaa ; bbb ; hi
10
20
'how are you'
>>> DeExport( 'aaa' ) ; Export( 'bbb' ) ; Export( 'hi' )
>>> a,b = B1( 'PrintPara "aaa=$aaa hi=$hi bbb=$bbb ~ `date`" "Hi there"' )
>>> print(a) ; print(b)
Num of Para. : 3
Para. $0 : PrintPara
Para. $1 : aaa= hi=how are you bbb=20 ~ Sat Oct 12 16:07:02 CST 2024
Para. $2 : Hi there
0
>>> a,b = B1( 'PrintPara "aaa=$aaa hi=\\$hi bbb=$bbb ~ `date`" "Hi there"' )
>>> print(a) ; print(b)
Num of Para. : 3
Para. $0 : PrintPara
Para. $1 : aaa=10 hi=$hi bbb= ~ Sat Oct 12 16:17:35 CST 2024
Para. $2 : Hi there
0
>>> Export( 'aaa' ) ; Export( 'bbb' ) ; Export( 'hi' )
>>> a,b = B1( 'PrintPara "aaa=$aaa hi=\\$hi \\" bbb=$bbb ~" "Hi \\" there"' )
>>> print(a) ; print(b)
Num of Para. : 3
Para. $0 : PrintPara
Para. $1 : aaa=10 hi=$hi " bbb=20 ~
Para. $2 : Hi " there
0
>>> 
>>> 
>>> a, b = B1( 'PrintPara1 ~, "How is it going???", $PWD' )
/bin/sh: PrintPara1: command not found
>>> 
'''

# from StartUpScript import *    # Be careful! This will reset some globals # needed if standalone

__os_environ_original__ = tuple( os.environ.keys() )

def Export( aVarName ) :
  '''Export( 'abc' ) : export the global var. named 'abc' as an environment variable.
  '''
    
  if aVarName not in tuple( globals().keys() ) :
    print( aVarName + ' not defined in the current Python session.' )
  elif globals()[ aVarName ] == None :
    print( aVarName + ' does not have any value.' )
  elif aVarName in __os_environ_original__ :
    print( aVarName + ' is an original environment variable. Cannot change its value.',  )
  else :
    # os.environ.__setitem__('hi', 'hello')
    # os.environ.__setitem__( aVarName, eval( ' + aVarName + ' )' ) )
    # os.environ.__setitem__( aVarName, repr( globals()[ aVarName ] ) )
    aValue = globals()[ aVarName ]
    if type( aValue ) is str :
      os.environ.__setitem__( aVarName, aValue )
    else :
      os.environ.__setitem__( aVarName, repr( aValue ) )
# Export()

def DeExport( aVarName ) :
  '''DeExport( 'abc' ) : make the (supposed) global var. named 'abc'a non-environment-variable
  '''
  
  # if aVarName not in tuple( globals().keys() ) :
  #   print( aVarName + ' not defined in the current Python session.' )
  # elif globals()[ aVarName ] == None :
  #   print( aVarName + ' does not have any value (and may not be an env. var.).' )
  # elif aVarName in __os_environ_original__ :
  if aVarName in __os_environ_original__ :
    print( aVarName + ' is an original environment variable. Cannot remove it.'  )
  else :
    os.environ.__delitem__( aVarName )
# DeExport()

def IsEnv( aVarName ) :
  '''IsEnv( 'abc' ) : checking whether the (supposed) global var. named 'abc' is an environment variable
  '''
  if aVarName in __os_environ_original__ :
    print( aVarName + ' is one of the original environment variables.'  )
  elif aVarName in tuple( os.environ ) :
    print( aVarName + ' is one of the newly added environment variables.' ) 
  else :
    print( aVarName + ' is not an environment variable.'  )
# IsEnv()

def PrintEnv( name ) :
  '''Print the value of the supposed environment variables with the given name
  '''
  print( os.getenv( name ) )
# PrintEnv()

def ChangeCWD( path ) :
  '''Change the current working directory (no path name expansion though)
  '''
  os.chdir( path.replace( '~', os.getenv( 'HOME' ) ) ) # chdir() itself does not support tilde expans.
# ChangeCWD()

def PrintCWD() :
  '''What is the current working directory?
  '''
  print( os.getcwd() )
# PrintCWD()

def PrintAllEV() :
  '''Print the list of all environment variables (names only)
  '''
  pprint( tuple( os.environ ) )
# PrintAllEV()

def PrintAllEV1() :
  '''Print the list of all envrionment variables (with values)
  '''
  pprint( dict( os.environ ) )
# PrintAllEV1()

def SyncEV() :
  '''Synchronize the values of those globals (that have been designated to be environment variables
  via the use of Export()) with their counterparts in os.environ (if there are any).
  '''
  
  for aVarName in tuple( os.environ.keys() ) :      # one of the current env. var.
    if aVarName not in __os_environ_original__ :    # not any of the original env. var.
      if aVarName in tuple( globals().keys() ) :    # still a global of current Python session
        if aVarName != '__os_environ_original__' :  # and is not __os_environ_original__
          # Update its value in os.environ{}
          aValue = globals()[ aVarName ]
          if type( aValue ) is str :
            os.environ.__setitem__( aVarName, aValue )
          else :
            os.environ.__setitem__( aVarName, repr( aValue ) )
  
# SyncEV()

def B( cmd ) : # redefine B() by adding SyncEV() ; we also need to make B() "one of ours"
  # '''B( cmd ) : Run a bash shell to execute cmd ; cmd should not contain >>'<<.
  '''B( cmd ) : Run a bash shell to execute cmd.
                Precede '\\\\' to any character appearing in cmd to cancel its special meaning.
     e.g.,
     >>> B( 'PrintPara "$PWD \\\\$PWD"' )  # There are two back-slashes in this example
     Num of Para. : 2
     Para. $0 : PrintPara
     Para. $1 : /Users/hsia/Pysh_Practice $PWD
  '''
  # cmd = "bash -c '" + cmd + "'"
  SyncEV()
  os.system( cmd )
# B()

def B1( cmd ) :  
  '''B1( cmd ) : Use bash to execute cmd and return two strings :
                 (1) the output (to stdin) of cmd, and (2) the final exit status of cmd
                 Precede '\\\\' to any character appearing in cmd to cancel its special meaning.
     e.g.,
     >>> a,b = B1( 'PrintPara "$PWD \\\\$PWD"' )  # there are two back-slashes in this example
     >>> print(a) ; print(b)
     Num of Para. : 2
     Para. $0 : PrintPara
     Para. $1 : /Users/hsia/Pysh_Practice $PWD
     0
  '''
  # cmd = "bash -c '" + cmd + "'"
  SyncEV()
  lines = os.popen( cmd + " ; echo $?" ).read().splitlines()
  outputStr = "\n".join( lines[:-1] )
  exitStatus = lines[-1]
  return outputStr, exitStatus

# B1()

### # Just use U() to execute Unix/Linux commands ; B( cmd ) : cmd cannot contain>>'<< ;
### 
### def U( cmd ) :
###   # '''U( cmd ) : Run a bash shell to execute cmd ; cmd should not contain >>'<<.
###   '''U( cmd ) : Run a bash shell to execute cmd.
###                 Precede '\\\\' to any character appearing in cmd to cancel its special meaning.
###      e.g.,
###      >>> U( 'PrintPara "$PWD \\\\$PWD"' )   # There are two back-slashes in this example
###      Num of Para. : 2
###      Para. $0 : PrintPara
###      Para. $1 : /Users/hsia/Pysh_Practice $PWD
###   '''
###   # cmd = "bash -c '" + cmd + "'"
###   SyncEV()
###   print( os.popen( cmd ).read(), end = '' )
### # U()
### 
### def U1( cmd ) :  
###   '''U1( cmd ) : Use bash to execute cmd and return two strings :
###                  (1) the output (to stdin) of cmd, and (2) the final exit status of cmd
###                  Precede '\\\\' to any character appearing in cmd to cancel its special meaning.
###      e.g.,
###      >>> a,b = U1( 'PrintPara "$PWD \\\\$PWD"' )  # there are two back-slashes in this example
###      >>> print(a) ; print(b)
###      Num of Para. : 2
###      Para. $0 : PrintPara
###      Para. $1 : /Users/hsia/Pysh_Practice $PWD
###      0
###   '''
###   # cmd = "bash -c '" + cmd + "'"
###   SyncEV()
###   lines = os.popen( cmd + " ; echo $?" ).read().splitlines()
###   outputStr = "\n".join( lines[:-1] )
###   exitStatus = lines[-1]
###   return outputStr, exitStatus
### # U1()

