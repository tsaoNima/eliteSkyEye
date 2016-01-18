'''
Created on Jan 17, 2016

@author: Me
'''
import log
import consoleListener
import constants
from structs import LogLevel

def testAll(pLog):
	#Get a connection to the log system.
	pLog.setLogFile("./testLogging.log")
	print "Got log instance."
	#Attach stdout listener.
	stdOut = consoleListener.ConsoleListener()
	stdOut.setLogLevel(LogLevel.Verbose)
	pLog.attach(stdOut)
	print "Attached console listener."
	print "Testing log output..."
	#Test all levels.
	pLog.logVerbose("Verbose message.")
	pLog.logDebug("Debug message.")
	pLog.logInfo("Info message.")
	pLog.logWarning("Warning message.")
	pLog.logError("Error message.")
	#Test tags.
	testTag = "testTag"
	stdOut.addTag(testTag)
	pLog.logInfo("This message should be visible to stdout...", constants.kTagAll)
	pLog.logInfo("But this one shouldn't!")
	pLog.logInfo("This message is tagged for stdout specifically.", testTag)
	
	print "Disconnecting from logger."
	pLog.detachAll()
	
if __name__ == "__main__":
	mLog = log.getLogInstance()
	testAll(mLog)
	mLog.shutdown()