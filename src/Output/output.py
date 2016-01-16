from enum import Enum

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
LogLevel = Enum("Verbose", "Info", "Warning", "Error")