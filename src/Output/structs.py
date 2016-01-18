'''
Created on Jan 15, 2016

@author: Me
'''
from enum import Enum
from collections import namedtuple

#Verbosity levels.
#Levels are for the following:
#	* Verbose: Debug information that wouldn't normally be reported.
#	* Info: Information that should be visible to administrators,
#	but is frequently posted on the order of seconds.
#	* Warning: Information on a non-critical problem.
#	* Error: Information on a critical problem; a request could not be completed.
#
#Each output module has its own echo level.
#In general, expected levels are:
#Console: Info
#Discord: Info
class LogLevel:
	Verbose = 0
	Debug = 1
	Info = 2
	Warning = 3
	Error = 4

#Describes one entry in the log buffer.
#TODO: should add timestamp.
LogElem = namedtuple("LogElem", "dateTime message logLevel tag")