'''
Created on Jan 17, 2016

@author: Me
'''
import log
import consoleListener
import constants
from structs import LogLevel

def testAll():
	#Get a connection to the log system.
	mLog = log.getLogInstance()
	mLog.setLogFile("./testLogging.log")
	print "Got log instance."
	#Attach stdout listener.
	stdOut = consoleListener.ConsoleListener()
	stdOut.setLogLevel(LogLevel.Verbose)
	mLog.subscribe(stdOut)
	print "Attached console listener."
	print "Testing log output..."
	#Test all levels.
	mLog.logVerbose("Verbose message.")
	mLog.logDebug("Debug message.")
	mLog.logInfo("Info message.")
	mLog.logWarning("Warning message.")
	mLog.logError("Error message.")
	#Test tags.
	testTag = "testTag"
	stdOut.addTag(testTag)
	mLog.logInfo("This message should be visible to stdout...", constants.kTagAll)
	mLog.logInfo("But this one shouldn't!")
	mLog.logInfo("This message is tagged for stdout specifically.", testTag)
	
	print "Shutting down logger."
	mLog.shutdown()