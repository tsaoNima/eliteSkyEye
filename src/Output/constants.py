'''
Created on Jan 16, 2016

@author: Me
'''

kLogBufferMaxLines = 1024
#Always open the log file for appending; don't truncate.
kLogFileMode = 'a+'

#All subscribers should print a message with this tag.
kTagAll = "*"
#This message is untagged.
kTagEmpty = ""

#Stdout constants.
kStrNone = "(none)"
kLogInShutdown = "Log.shutdown(): Logger is going down NOW"
kFmtLogSubscribeFailed = "Log.subscribe(): Can't attach subscriber {0}, subscriber doesn't derive from OutputBase!"
kFmtLogOpeningLogFile = "setLogFile(): Opening log file {0}"
kFmtLogClosingLogFile = "setLogFile(): Closing log file {0}"
kFmtLogSwitchedLogFile = "setLogFile(): Switched to log file {0}"
kFmtLogFileOpenFailed = "setLogFile(): Couldn't open \"{0}\", aborting!\nReason: {1}"
kLogNoFileOpen = "setLogFile(): No log file specified, buffer will not be saved!"