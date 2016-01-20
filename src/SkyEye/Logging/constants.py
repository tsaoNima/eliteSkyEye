'''
Created on Jan 16, 2016

@author: Me
'''
from structs import LogLevel

kLogBufferMaxLines = 1024
#Always open the log file for appending; don't truncate.
kLogFileMode = 'a+'

#All subscribers should print a message with this tag.
kTagAll = "*"
#This message is untagged.
kTagEmpty = ""

#Sender didn't specify where in the program this message was sent.
kWhereUnknown = "(unknown function)"

#Log file constants.
kFmtLogFileLine = "[{0}] {1}@{2}({3}): {4}"
"""Format line used for writing to a log file. Parameters:
0: Time the message was logged.
1: Log level.
2: Where the message was sent from.
3: Tag.
4: Message.
"""

kLogLevelNames = {
				LogLevel.Verbose : "V",
				LogLevel.Debug : "D",
				LogLevel.Info : "I",
				LogLevel.Warning : "W",
				LogLevel.Error : "E"
				}

kFmtStdOutLine = "[{0}] @{1}({2}): {3}"
"""Format line used for writing to a console listener. Parameters:
0: Time the message was logged.
1: Where the message was sent from.
2: Tag.
3: Message.
"""

#Stdout constants.
kStrNone = "(none)"
kLogInitComplete = "Log.__init__(): Logger ready, opening log file"
kLogInShutdown = "Log.shutdown(): Logger is going down NOW"
kFmtLogSubscribeFailed = "Log.subscribe(): Can't attach subscriber {0}, subscriber doesn't derive from OutputBase!"
kFmtLogOpeningLogFile = "setLogFile(): Opening log file {0}"
kFmtLogClosingLogFile = "setLogFile(): Closing log file {0}"
kFmtLogSwitchedLogFile = "setLogFile(): Switched to log file {0}"
kFmtLogFileOpenFailed = "setLogFile(): Couldn't open \"{0}\", aborting!\nReason: {1}"
kLogNoFileOpen = "setLogFile(): No log file specified, buffer will not be saved!"