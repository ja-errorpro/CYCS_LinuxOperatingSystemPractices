#!/usr/bin/env python3.11
# -*- coding: utf_8 -*-

# To use a coding scheme other than UTF-8, put, e.g., '# -*- coding: cp1252 -*-' on this (i.e., the 2nd) line, where 'cp1252' (Windows-1252) must be a valid codecs supported by Python.

# # what are the encodings that python supports  # 'virtualenv' and 've' use cp1252 to decode this file
# import encodings
# pp( sorted( set( encodings.aliases.aliases.values() ) ) )

import os
import subprocess
import sys
from pprint import pprint
import importlib

def pp( obj ) : # the pprint module also has pp(), a wrapper of pprint() ; here, we define our own
  pprint( obj, width = 1, indent = 2 )

# so, pp() is our own (a specialized pprint.pprint()), while pprint() is the original pprint.pprint()

## Since we now have B(), L() should not be needed.
## One "drawback" with L() is that it runs 'cmd' in the background,
## causing '>>>' to be displayed before the output of 'cmd' is displayed,
## making it look like the user is not prompted after the output of 'cmd' appears.

# def L( cmd ) :
#   subprocess.Popen( cmd, shell=True, executable='/bin/bash' )

# Supposedly, 'S' should mean 'sh' (the shell that is used to run the 'cmd'
# As it turned out, os.system() uses 'bash' to run the command ...

# def S( cmd ) :
#   '''S( cmd ) : Run sh to execute cmd ; cmd should not contain >>'<<.
#                 Precede '\\\\' to any character appearing in cmd to cancel its special meaning.
#      e.g.,
#      >>> S( 'PrintPara "$PWD \\\\$PWD"' )  # There are two back-slashes in this example
#      Num of Para. : 2
#      Para. $0 : PrintPara
#      Para. $1 : /Users/usrID/Pysh_Practice $PWD
#   '''
#   os.system( cmd )

# 'B' means 'bash' ;
#
# Remember to always use >>' ... '<< to specify a bash-command (i.e., use single-quotes for specifying the cmd-string).
# In specifying the command itself (i.e., the >>...<< of >>'...'<<), use >>"<< as much as possible.
# e.g.,
# B( 'LANG=zh_TW.UTF-8 ; var123="The dollar expression \$(( 3 + 5 )) will give us $((3+5)), while \`date\` will give us `date`" ; echo $var123 ' )
#
# If the use of >>'<< is absolutely necessary for specifying the bash-command to execute, see if >>\'<< will work.
# However, there is no guarantee (that >>\'<< will work).
#
# Of course, we can also run >>B( './BashTestScript.sh' )<< to simplify typing.
# But to try to prevent from potential hacking, the file permission bits of this shell script (e.g., BashTestScript.sh)
# should be such that the 'setuid' and 'setgid' bits are both set (i.e., do >>chmod 7755 BashTestScript.sh<< in advance)

def B( cmd ) :
  # os.system( "bash -c '" + cmd + "'" )
  os.system( cmd )

with open( os.getenv( 'HOME' ) + '/bin/Environ.py' ) as file123 :
  exec( file123.read() )

del( file123 )

STR = str
LEN = len
INT = int

# Better not print below, so as not to distort the output
print('\nPython %s on %s' % (sys.version, sys.platform))
print( "\n--- StartUpScript.py loaded ---\n" )

